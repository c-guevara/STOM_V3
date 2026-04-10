
import binance
import pandas as pd
from PyQt5.QtCore import QTimer
from traceback import format_exc
from trade.base_trader import BaseTrader
from utility.setting_base import ui_num, columns_jgcf
from trade.binance.binance_websocket import WebSocketTrader
from utility.static import now, timedelta_sec, error_decorator, get_binance_short_profit, get_binance_long_profit


class BinanceTrader(BaseTrader):
    def __init__(self, qlist, dict_set, market_infos):
        super().__init__(qlist, dict_set, market_infos)

        self.dict_order = {
            'BUY_LONG': {},
            'SELL_LONG': {},
            'SELL_SHORT': {},
            'BUY_SHORT': {}
        }

        access_key = self.dict_set[f"access_key{self.market_info['계정번호']}"]
        secret_key = self.dict_set[f"secret_key{self.market_info['계정번호']}"]

        self.binance = binance.Client(access_key, secret_key)

        self._get_balances()

        if not self.dict_set['모의투자']:
            self.ws_thread = WebSocketTrader(access_key, secret_key, self.windowQ)
            self.ws_thread.signal.connect(self._convert_order_data)
            self.ws_thread.start()

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

    def _update_jango(self, data):
        종목코드, 현재가 = data
        self.dict_curc[종목코드] = 현재가
        try:
            """['종목명', '포지션', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수',
                '분할매도횟수', '매수시간']"""
            if 현재가 != self.dict_jg[종목코드]['현재가']:
                포지션 = self.dict_jg[종목코드]['포지션']
                매입금액 = self.dict_jg[종목코드]['매입금액']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                if 포지션 == 'LONG':
                    평가금액, 평가손익, 수익률 = get_binance_long_profit(
                        매입금액,
                        보유수량 * 현재가,
                        '시장가' in self.dict_set['매수주문유형'],
                        '시장가' in self.dict_set['매도주문유형']
                    )
                else:
                    평가금액, 평가손익, 수익률 = get_binance_short_profit(
                        매입금액,
                        보유수량 * 현재가,
                        '시장가' in self.dict_set['매수주문유형'],
                        '시장가' in self.dict_set['매도주문유형']
                    )
                self.dict_jg[종목코드].update({
                    '현재가': 현재가,
                    '수익률': 수익률,
                    '평가손익': 평가손익,
                    '평가금액': 평가금액
                })
        except:
            pass

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

    def _cancel_order(self, 종목코드, 주문구분):
        종목명 = self.dict_info[종목코드]['종목명']
        last_value = self._get_chejan_last_value(종목코드, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                주문번호, 주문가격 = last_value['주문번호'], last_value['주문가격']
                self._create_order(f'{주문구분}_CANCEL', 종목코드, 종목명, 주문가격, 미체결수량, 주문번호, now(), False, 0, None)

    def _modify_order(self, 종목코드, 주문구분):
        last_value = self._get_chejan_last_value(종목코드, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                if 주문구분 == 'BUY_LONG':
                    정정가격 = self.dict_curc[종목코드] - self.dict_order[주문구분][종목코드][3] * self.dict_set['매수정정호가']
                elif 주문구분 == 'SELL_SHORT':
                    정정가격 = self.dict_curc[종목코드] + self.dict_order[주문구분][종목코드][3] * self.dict_set['매수정정호가']
                elif 주문구분 == 'SELL_LONG':
                    정정가격 = self.dict_curc[종목코드] + self.dict_order[주문구분][종목코드][3] * self.dict_set['매도정정호가']
                else:
                    정정가격 = self.dict_curc[종목코드] - self.dict_order[주문구분][종목코드][3] * self.dict_set['매도정정호가']

                현재시간 = now()
                정정횟수 = self.dict_order[주문구분][종목코드][1] + 1
                주문번호, 주문가격 = last_value['주문번호'], last_value['주문가격']
                self._create_order(f'{주문구분}_CANCEL', 종목코드, 종목코드, 주문가격, 미체결수량, 주문번호, 현재시간, False, 0, None)
                self._create_order(주문구분, 종목코드, 종목코드, 정정가격, 미체결수량, '', 현재시간, False, 정정횟수, None)

    def _jango_cheongsan(self, gubun):
        for 주문구분 in self.dict_order:
            for 종목코드 in self.dict_order[주문구분]:
                self._cancel_order(종목코드, 주문구분)

        if self.dict_jg:
            if gubun == '수동':
                self.teleQ.put('잔고청산 주문을 전송합니다.')
            for 종목코드 in self.dict_jg.copy():
                포지션 = self.dict_jg[종목코드]['포지션']
                현재가 = self.dict_jg[종목코드]['현재가']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                주문구분 = 'SELL_LONG' if 포지션 == 'LONG' else 'BUY_SHORT'
                if self.dict_set['모의투자']:
                    주문시간 = self._get_str_ymdhms()
                    self._update_chejan_data(주문구분, 종목코드, 보유수량, 보유수량, 0, 현재가, 현재가, 주문시간, '')
                else:
                    self._check_order((주문구분, 종목코드, 현재가, 보유수량, now(), True))
            if self.dict_set['알림소리']:
                self.soundQ.put('잔고청산 주문을 전송하였습니다.')
            self.windowQ.put((ui_num['기본로그'], '시스템 명령 실행 알림 - 잔고청산 주문 완료'))
        elif gubun == '수동':
            self.teleQ.put('현재는 보유종목이 없습니다.')
        self.dict_bool['잔고청산'] = True

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
                    평가금액 = round(체결가격 * 보유수량, 4)
                    if 주문구분 == 'BUY_LONG':
                        평가금액, 수익금, 수익률 = get_binance_long_profit(
                            매입금액,
                            평가금액,
                            '시장가' in self.dict_set['매수주문유형'],
                            '시장가' in self.dict_set['매도주문유형']
                        )
                    else:
                        평가금액, 수익금, 수익률 = get_binance_short_profit(
                            매입금액,
                            평가금액,
                            '시장가' in self.dict_set['매수주문유형'],
                            '시장가' in self.dict_set['매도주문유형']
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
                    매입금액 = round(체결가격 * 체결수량, 4)
                    if self.dict_set['바이낸스선물고정레버리지']:
                        레버리지 = self.dict_set['바이낸스선물고정레버리지값']
                    else:
                        레버리지 = self.dict_order[주문구분][종목코드][4]
                    if 주문구분 == 'BUY_LONG':
                        포지션 = 'LONG'
                        평가금액, 수익금, 수익률 = get_binance_long_profit(
                            매입금액,
                            매입금액,
                            '시장가' in self.dict_set['매수주문유형'],
                            '시장가' in self.dict_set['매도주문유형']
                        )
                    else:
                        포지션 = 'SHORT'
                        평가금액, 수익금, 수익률 = get_binance_short_profit(
                            매입금액,
                            매입금액,
                            '시장가' in self.dict_set['매수주문유형'],
                            '시장가' in self.dict_set['매도주문유형']
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
                    평가금액 = round(체결가격 * 보유수량, 4)
                    if 주문구분 == 'SELL_LONG':
                        평가금액, 수익금, 수익률 = get_binance_long_profit(
                            매입금액,
                            평가금액,
                            '시장가' in self.dict_set['매수주문유형'],
                            '시장가' in self.dict_set['매도주문유형']
                        )
                    else:
                        평가금액, 수익금, 수익률 = get_binance_short_profit(
                            매입금액,
                            평가금액,
                            '시장가' in self.dict_set['매수주문유형'],
                            '시장가' in self.dict_set['매도주문유형']
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
                평가금액 = round(체결가격 * 체결수량, 4)
                if 주문구분 == 'SELL_LONG':
                    평가금액, 수익금, 수익률 = get_binance_long_profit(
                        매입금액,
                        평가금액,
                        '시장가' in self.dict_set['매수주문유형'],
                        '시장가' in self.dict_set['매도주문유형']
                    )
                else:
                    평가금액, 수익금, 수익률 = get_binance_short_profit(
                        매입금액,
                        평가금액,
                        '시장가' in self.dict_set['매수주문유형'],
                        '시장가' in self.dict_set['매도주문유형']
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
