
import sys
import binance
import pandas as pd
from PyQt5.QtCore import QTimer
from traceback import format_exc
from PyQt5.QtWidgets import QApplication
from utility.setting_base import ui_num, columns_jgcf
from trade.base_trader import BaseTrader, MonitorTraderQ
from utility.static import now, timedelta_sec, error_decorator, get_profit_coin_future_short, \
    get_profit_coin_future_long


class BinanceTrader(BaseTrader):
    def __init__(self, qlist, dict_set, market_infos):
        super().__init__(qlist, dict_set, market_infos)

        app = QApplication(sys.argv)

        self.dict_order = {
            'BUY_LONG': {},
            'SELL_LONG': {},
            'SELL_SHORT': {},
            'BUY_SHORT': {}
        }

        self.binance = binance.Client(self.access_key, self.secret_key)

        self._get_balances()

        if not self.dict_set['모의투자']:
            from trade.binance.binance_websocket import BinanceWebSocketTrader
            self.ws_thread = BinanceWebSocketTrader(self.access_key, self.secret_key, self.windowQ)
            self.ws_thread.signal.connect(self._convert_order_data)
            self.ws_thread.start()

        self.qtimer1 = QTimer()
        self.qtimer1.setInterval(500)
        self.qtimer1.timeout.connect(self._scheduler1)
        self.qtimer1.start()

        self.qtimer2 = QTimer()
        self.qtimer2.setInterval(1 * 1000)
        self.qtimer2.timeout.connect(self._scheduler2)
        self.qtimer2.start()

        self.updater = MonitorTraderQ(self.traderQ, self.market_gubun)
        self.updater.signal1.connect(self._check_order)
        self.updater.signal2.connect(self._check_order_future)
        self.updater.signal3.connect(self._update_tuple)
        self.updater.signal4.connect(self._update_string)
        self.updater.start()

        app.exec_()

    def _get_balances(self):
        if self.dict_set['모의투자']:
            yesugm = self._get_yesugm_for_paper_trading()
        else:
            datas = self.binance.futures_account_balance()
            yesugm = [float(data['balance']) for data in datas if data['asset'] == 'USDT'][0]
        self._set_yesugm_and_noti(yesugm)

    def _send_order(self, data):
        curr_time = now()
        if curr_time < self.order_time:
            next_time = (self.order_time - curr_time).total_seconds()
            QTimer.singleShot(int(next_time * 1000), lambda: self._send_order(data))
            return

        주문구분, 종목코드, 종목명, 주문가격, 주문수량, 원주문번호, 시그널시간, 잔고청산, 정정횟수, 수동주문유형 = data
        매도수구분, 포지션 = 주문구분.split('_')[:2]
        self._order_time_log(시그널시간)
        if 'CANCEL' not in 주문구분:
            ret = None
            if 수동주문유형 == '시장가' or (수동주문유형 is None and self.dict_set['매수주문유형'] == '시장가') or 잔고청산:
                ret = self.binance.futures_create_order(
                    symbol=종목코드, side=매도수구분, type='MARKET', quantity=주문수량
                )
            elif 수동주문유형 == '지정가' or (수동주문유형 is None and self.dict_set['매수주문유형'] == '지정가'):
                ret = self.binance.futures_create_order(
                    symbol=종목코드, side=매도수구분, type='LIMIT', price=주문가격, timeInForce='GTC', quantity=주문수량
                )
            elif 수동주문유형 == '지정가IOC' or (수동주문유형 is None and self.dict_set['매수주문유형'] == '지정가IOC'):
                ret = self.binance.futures_create_order(
                    symbol=종목코드, side=매도수구분, type='LIMIT', price=주문가격, timeInForce='IOC', quantity=주문수량
                )
            elif 수동주문유형 == '지정가FOK' or (수동주문유형 is None and self.dict_set['매수주문유형'] == '지정가FOK'):
                ret = self.binance.futures_create_order(
                    symbol=종목코드, side=매도수구분, type='LIMIT', price=주문가격, timeInForce='FOK', quantity=주문수량
                )

            if ret is not None:
                if 주문구분 in ('BUY_LONG', 'SELL_SHORT'):
                    self.dict_intg['추정예수금'] -= 주문수량 * 주문가격
                    add_time = self.dict_set['매수취소시간초']
                else:
                    add_time = self.dict_set['매도취소시간초']

                self.dict_order[주문구분][종목코드] = [
                    timedelta_sec(add_time), 정정횟수, 주문가격, self.dict_info[종목코드]['호가단위'], self.dict_lvrg[종목코드]
                ]

                self.dict_pos[종목코드] = 포지션

                # noinspection PyUnresolvedReferences
                orderId = int(ret['orderId'])
                index = self._get_index()
                self._update_chegeollist(index, 종목코드, 종목명, f'{주문구분}_REG', 주문수량, 0, 주문수량, 0, index[:14], 주문가격, orderId)
                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분}_REG] {종목코드} | {주문가격} | {주문수량}'
                ))
            else:
                self._put_order_complete(f'{주문구분}_CANCEL', 종목코드)
                self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'))
        else:
            ret = self.binance.futures_cancel_order(symbol=종목코드, orderId=원주문번호)
            if ret is not None:
                self.dict_pos[종목코드] = 포지션
            else:
                self.windowQ.put((
                    ui_num['기본로그'],
                    f'{format_exc()}\n주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'
                ))

        self.order_time = timedelta_sec(0.2)
        self.receivQ.put(('주문목록', self._get_order_code_list()))

    def _set_position(self):
        if self.dict_set['바이낸스선물고정레버리지']:
            self.dict_lvrg = {x: self.dict_set['바이낸스선물고정레버리지값'] for x in self.dict_info}
        else:
            self.dict_lvrg = {x: 1 for x in self.dict_info}

        if not self.dict_set['모의투자']:
            for code in self.dict_info:
                try:
                    if self.dict_set['바이낸스선물고정레버리지']:
                        self.binance.futures_change_leverage(symbol=code, leverage=self.dict_set['바이낸스선물고정레버리지값'])
                    else:
                        self.binance.futures_change_leverage(symbol=code, leverage=1)
                    self.binance.futures_change_margin_type(symbol=code, marginType=self.dict_set['바이낸스선물마진타입'])
                except:
                    pass
            try:
                self.binance.futures_change_position_mode(dualSidePosition=self.dict_set['바이낸스선물포지션'])
            except:
                pass

        self.windowQ.put((ui_num['기본로그'], '시스템 명령 실행 알림 - 마진타입 및 레버리지 설정 완료'))

    def _set_leverage(self, dict_dlhp):
        for code in self.dict_info:
            lhp = dict_dlhp.get(code)
            if lhp:
                try:
                    leverage = self._get_leverage(lhp[1])
                    self.dict_lvrg[code] = leverage
                    if not self.dict_set['모의투자']:
                        self.binance.futures_change_leverage(symbol=code, leverage=leverage)
                except:
                    pass

    def _get_leverage(self, lhp):
        leverage = 1
        for min_area, max_area, lvrg in self.dict_set['바이낸스선물변동레버리지값']:
            if min_area <= lhp < max_area:
                leverage = lvrg
                break
        return leverage

    def _convert_order_data(self, data):
        if data['e'] == 'ACCOUNT_UPDATE':
            try:
                bal_list = data['a']['B']
                for bal_dict in bal_list:
                    if bal_dict['a'] == 'USDT':
                        self.dict_intg['추정예탁자산'] = float(bal_dict['wb'])
                        self.dict_intg['예수금'] = float(bal_dict['cw'])
                        break
            except:
                self.windowQ.put((ui_num['시스템로그'], f'{format_exc()}오류 알림 - 유저 웹소켓'))
        elif data['e'] == 'ORDER_TRADE_UPDATE':
            try:
                data = data['o']
                code = data['s']
                p = f"{data['S']}_{self.dict_pos[code]}"
                if data['X'] == 'CANCELED':
                    p = f'{p}_CANCEL'
                oc = float(data['q'])
                cc = float(data['l'])
                mc = round(oc - float(data['z']), self.dict_info[code]['소숫점자리수'])
                cp = float(data['L'])
                op = float(data['p'])
                on = int(data['i'])
            except:
                self.windowQ.put((ui_num['시스템로그'], f'{format_exc()}오류 알림 - 바이낸스 홈페이지 주문은 기록되지 않습니다.'))
            else:
                if cc > 0 or 'CANCEL' in p:
                    ct = self._get_str_ymdhms()
                    self._update_chejan_data(p, code, oc, cc, mc, cp, op, ct, on)

    @error_decorator
    def _update_chejan_data(self, 주문구분, 종목코드, 주문수량, 체결수량, 미체결수량, 체결가격, 주문가격, 주문시간, 주문번호):
        index = self._get_index()
        종목명 = self.dict_info[종목코드]['종목명']

        if 주문구분 in ('BUY_LONG', 'SELL_SHORT', 'SELL_LONG', 'BUY_SHORT'):
            if 주문구분 in ('BUY_LONG', 'SELL_SHORT'):
                # ['종목명', '포지션', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간', '레버리지']
                if 종목코드 in self.dict_jg:
                    보유수량 = round(self.dict_jg[종목코드]['보유수량'] + 체결수량, self.dict_info[종목코드]['소숫점자리수'])
                    매입금액 = round(self.dict_jg[종목코드]['매입금액'] + 체결수량 * 체결가격, 4)
                    매수가 = round(매입금액 / 보유수량, 8)
                    보유금액 = round(체결가격 * 보유수량, 4)
                    if 주문구분 == 'BUY_LONG':
                        평가금액, 수익금, 수익률 = get_profit_coin_future_long(
                            매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                        )
                    else:
                        평가금액, 수익금, 수익률 = get_profit_coin_future_short(
                            매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                        )
                    self.dict_jg[종목코드].update({
                        '매수가': 매수가,
                        '현재가': 체결가격,
                        '수익률': 수익률,
                        '평가손익': 수익금,
                        '매입금액': 매입금액,
                        '평가금액': 평가금액,
                        '보유수량': 보유수량,
                        '매수시간': 주문시간
                    })
                else:
                    매입금액 = 보유금액 = round(체결가격 * 체결수량, 4)
                    if self.dict_set['바이낸스선물고정레버리지']:
                        레버리지 = self.dict_set['바이낸스선물고정레버리지값']
                    else:
                        레버리지 = self.dict_order[주문구분][종목코드][4]
                    if 주문구분 == 'BUY_LONG':
                        포지션 = 'LONG'
                        평가금액, 수익금, 수익률 = get_profit_coin_future_long(
                            매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                        )
                    else:
                        포지션 = 'SHORT'
                        평가금액, 수익금, 수익률 = get_profit_coin_future_short(
                            매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                        )
                    self.dict_jg[종목코드] = {
                        '종목명': 종목명,
                        '포지션': 포지션,
                        '매수가': 체결가격,
                        '현재가': 체결가격,
                        '수익률': 수익률,
                        '평가손익': 수익금,
                        '매입금액': 매입금액,
                        '평가금액': 평가금액,
                        '보유수량': 체결수량,
                        '분할매수횟수': 0,
                        '분할매도횟수': 0,
                        '매수시간': 주문시간,
                        '레버리지': 레버리지
                    }

                if 미체결수량 == 0:
                    self.dict_jg[종목코드]['분할매수횟수'] += 1
                    if 종목코드 in self.dict_order[주문구분]:
                        del self.dict_order[주문구분][종목코드]

            else:
                if 종목코드 not in self.dict_jg: return
                포지션 = self.dict_jg[종목코드]['포지션']
                매수가 = self.dict_jg[종목코드]['매수가']
                보유수량 = round(self.dict_jg[종목코드]['보유수량'] - 체결수량, self.dict_info[종목코드]['소숫점자리수'])
                if 보유수량 != 0:
                    매입금액 = round(매수가 * 보유수량, 4)
                    보유금액 = round(체결가격 * 보유수량, 4)
                    if 주문구분 == 'SELL_LONG':
                        평가금액, 수익금, 수익률 = get_profit_coin_future_long(
                            매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                        )
                    else:
                        평가금액, 수익금, 수익률 = get_profit_coin_future_short(
                            매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                        )
                    """['종목명', '포지션', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량',
                        '분할매수횟수', '분할매도횟수', '매수시간', '레버리지']"""
                    self.dict_jg[종목코드].update({
                        '현재가': 체결가격,
                        '수익률': 수익률,
                        '평가손익': 수익금,
                        '매입금액': 매입금액,
                        '평가금액': 평가금액,
                        '보유수량': 보유수량
                    })
                else:
                    del self.dict_jg[종목코드]

                if 미체결수량 == 0:
                    if 보유수량 > 0:
                        self.dict_jg[종목코드]['분할매도횟수'] += 1
                    if 종목코드 in self.dict_order[주문구분]:
                        del self.dict_order[주문구분][종목코드]

                매입금액 = round(매수가 * 체결수량, 4)
                보유금액 = round(체결가격 * 체결수량, 4)
                if 주문구분 == 'SELL_LONG':
                    평가금액, 수익금, 수익률 = get_profit_coin_future_long(
                        매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                    )
                else:
                    평가금액, 수익금, 수익률 = get_profit_coin_future_short(
                        매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
                    )
                if -100 < 수익률 < 100:
                    self._update_tradelist(index, 종목명, 포지션, 매입금액, 평가금액, 체결수량, 수익률, 수익금, 주문시간)
                if 수익률 < 0: self.dict_info[종목코드]['손절거래시간'] = timedelta_sec(self.dict_set['매수금지손절간격초'])

            self.dict_jg = dict(sorted(self.dict_jg.items(), key=lambda x: x[1]['매입금액'], reverse=True))

            if 미체결수량 == 0:
                self._put_order_complete(f'{주문구분}_COMPLETE', 종목코드)
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

            if self.dict_set['모의투자']:
                if 주문구분 in ('BUY_LONG', 'SELL_SHORT'):
                    self.dict_intg['예수금'] -= 체결수량 * 체결가격
                    self.dict_intg['추정예수금'] -= 체결수량 * 체결가격
                else:
                    self.dict_intg['예수금'] += 매입금액 + 수익금
                    self.dict_intg['추정예수금'] += 매입금액 + 수익금

            if self.dict_jg:
                df_jg = pd.DataFrame.from_dict(self.dict_jg, orient='index')
            else:
                df_jg = pd.DataFrame(columns=columns_jgcf)
            self.queryQ.put(('거래디비', df_jg, self.market_info['잔고디비'], 'replace'))
            if self.dict_set['알림소리']:
                text = ''
                if 주문구분 == 'BUY_LONG':     text = '롱포지션을 진입'
                elif 주문구분 == 'SELL_SHORT': text = '숏포지션을 진입'
                elif 주문구분 == 'SELL_LONG':  text = '롱포지션을 청산'
                elif 주문구분 == 'BUY_SHORT':  text = '숏포지션을 청산'
                self.soundQ.put(f"{종목코드} {text}하였습니다.")
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분}] {종목명} | {체결가격} | {체결수량}'))

        elif 주문구분 == '시드부족':
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

        elif 주문구분 in ('BUY_LONG_CANCEL', 'SELL_SHORT_CANCEL', 'SELL_LONG_CANCEL', 'BUY_SHORT_CANCEL'):
            if 주문구분 in ('BUY_LONG_CANCEL', 'SELL_SHORT_CANCEL'):
                self.dict_intg['추정예수금'] += 주문수량 * 주문가격

            gubun_ = 주문구분.replace('_CANCEL', '')
            if 종목코드 in self.dict_order[gubun_]:
                del self.dict_order[gubun_][종목코드]

            self._put_order_complete(주문구분, 종목코드)
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

            if self.dict_set['알림소리']:
                text = ''
                if 주문구분 == 'BUY_LONG_CANCEL':     text = '롱포지션 진입을 취소'
                elif 주문구분 == 'SELL_SHORT_CANCEL': text = '숏포지션 진입을 취소'
                elif 주문구분 == 'SELL_LONG_CANCEL':  text = '롱포지션 청산을 취소'
                elif 주문구분 == 'BUY_SHORT_CANCEL':  text = '숏포지션 청산을 취소'
                self.soundQ.put(f"{종목코드} {text}하였습니다.")
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분}] {종목명} | {주문가격} | {주문수량}'))

        self.receivQ.put(('잔고목록', tuple(self.dict_jg)))
        self.receivQ.put(('주문목록', self._get_order_code_list()))
