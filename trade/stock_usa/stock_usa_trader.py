
import pandas as pd
from PyQt5.QtCore import QTimer
from trade.base_trader import BaseTrader
from utility.setting_base import ui_num,  columns_jg
from trade.ls_rest_api import LsRestAPI, WebSocketTrader
from utility.static import now, timedelta_sec, error_decorator, get_stock_os_profit


class StockUsaTrader(BaseTrader):
    def __init__(self, qlist, dict_set, market_infos):
        super().__init__(qlist, dict_set, market_infos)

        self.dict_order = {
            '매수': {},
            '매도': {},
            '매수취소': {},
            '매도취소': {}
        }

        access_key = self.dict_set[f"access_key{self.market_info['계정번호']}"]
        secret_key = self.dict_set[f"secret_key{self.market_info['계정번호']}"]

        self.ls = LsRestAPI(self.windowQ, access_key, secret_key)
        self.token = self.ls.create_token()

        if not self.dict_set['모의투자']:
            self.ws_thread = WebSocketTrader(self.market_info['마켓이름'], self.token, self.windowQ)
            self.ws_thread.signal.connect(self._convert_order_data)
            self.ws_thread.start()

        self._get_balances()

    def _get_balances(self):
        if self.dict_set['모의투자']:
            yesugm = self._get_yesugm_for_paper_trading()
        else:
            yesugm = self.ls.get_balance_stock_usa()
        self._set_yesugm_and_noti(yesugm)

    def _send_order(self, data):
        curr_time = now()
        if curr_time < self.order_time:
            next_time = (self.order_time - curr_time).total_seconds()
            QTimer.singleShot(int(next_time * 1000), lambda: self._send_order(data))
            return

        주문구분, 종목코드, 종목명, 주문가격, 주문수량, 원주문번호, 시그널시간, 잔고청산, 정정횟수, 수동주문유형 = data
        주문시장코드 = self.dict_info[종목코드]['거래소코드']
        self._order_time_log(시그널시간)

        if 주문구분 in ('매수', '매도'):
            if 잔고청산:
                주문유형 = '시장가'
            else:
                주문유형 = self.dict_set[f'{주문구분}주문유형'] if 수동주문유형 is None else 수동주문유형

            """def order_stock_usa(self, 종목코드, 주문구분, 주문시장코드, 주문수량, 주문가격, 호가유형, 원주문번호=''):"""
            od_no, msg = self.ls.order_stock_usa(종목코드, 주문구분, 주문시장코드, 주문수량, 주문가격, 주문유형)
            if od_no != '0':
                index = self._get_index()
                if 주문구분 == '매수':
                    self.dict_intg['추정예수금'] -= 주문수량 * 주문가격
                    add_time = self.dict_set['매수취소시간초']
                else:
                    add_time = self.dict_set['매도취소시간초']

                self.dict_order[주문구분][종목코드] = [
                    timedelta_sec(add_time), 정정횟수, 주문가격, 0.01
                ]

                self._update_chegeollist(
                    index, 종목코드, 종목명, f'{주문구분} 접수', 주문수량, 0, 주문수량, 0, index[:14], 주문가격, od_no
                )

                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 접수] {종목명} | {주문가격} | {주문수량}'
                ))
            else:
                self._put_order_complete('매수취소', 종목코드)
                self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'))
                self.windowQ.put((ui_num['기본로그'], msg))

        elif 주문구분 in ('매수정정', '매도정정'):
            """def order_modify_stock_usa(self, 종목코드, 원주문번호, 주문구분, 주문시장코드, 주문수량, 주문가격, 호가유형):"""
            주문구분_ = 주문구분[:2]
            주문유형 = self.dict_set[f'{주문구분_}주문유형']
            od_no, msg = self.ls.order_modify_stock_usa(종목코드, 원주문번호, 주문구분_, 주문시장코드, 주문수량, 주문가격, 주문유형)
            if od_no == '0':
                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'
                ))
                self.windowQ.put((ui_num['기본로그'], msg))

        elif 주문구분 in ('매수취소', '매도취소'):
            """def order_stock_usa(self, 종목코드, 주문구분, 주문시장코드, 주문수량, 주문가격, 호가유형, 원주문번호=''):"""
            주문유형 = self.dict_set[f'{주문구분[:2]}주문유형'] if 수동주문유형 is None else 수동주문유형
            od_no, msg = self.ls.order_stock_usa(종목코드, '취소', 주문시장코드, 주문수량, 주문가격, 주문유형, 원주문번호)
            if od_no == '0':
                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량} | {주문구분}'
                ))
                self.windowQ.put((ui_num['기본로그'], msg))

        self.order_time = timedelta_sec(0.2)
        self.receivQ.put(('주문목록', self._get_order_code_list()))

    def _update_Jango(self, data):
        종목코드, 현재가 = data
        self.dict_curc[종목코드] = 현재가
        try:
            """['종목명', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량',
                '분할매수횟수', '분할매도횟수', '매수시간']"""
            if 현재가 != self.dict_jg[종목코드]['현재가']:
                매입금액 = self.dict_jg[종목코드]['매입금액']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                평가금액, 평가손익, 수익률 = get_stock_os_profit(매입금액, 보유수량 * 현재가)
                self.dict_jg[종목코드].update({
                    '현재가': 현재가,
                    '수익률': 수익률,
                    '평가손익': 평가손익,
                    '평가금액': 평가금액
                })
        except:
            pass

    def _cancel_order(self, 종목코드, 주문구분):
        종목명 = self.dict_info[종목코드]['종목명']
        last_value = self._get_chejan_last_value(종목명, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                주문번호, 주문가격 = last_value['주문번호'], last_value['주문가격']
                self._create_order('취소', 종목코드, 종목명, 주문가격, 미체결수량, 주문번호, now(), False, 0, None)

    def _modify_order(self, 종목코드, 주문구분):
        종목명 = self.dict_info[종목코드]['종목명']
        last_value = self._get_chejan_last_value(종목코드, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                if 주문구분 == '매수':
                    주문가격 = self.dict_curc[종목코드] - self.dict_order[주문구분][종목코드][3] * self.dict_set['매수정정호가']
                else:
                    주문가격 = self.dict_curc[종목코드] + self.dict_order[주문구분][종목코드][3] * self.dict_set['매도정정호가']

                현재시간 = now()
                정정횟수 = self.dict_order[주문구분][종목코드][1] + 1
                원주문번호 = last_value['주문번호']
                self._create_order(f'{주문구분}정정', 종목코드, 종목명, 주문가격, 미체결수량, 원주문번호, 현재시간, False, 정정횟수, None)

    def _jango_cheongsan(self, gubun):
        for 주문구분 in self.dict_order:
            if 주문구분 in ('매수', '매도'):
                for 종목코드 in self.dict_order[주문구분]:
                    self._cancel_order(종목코드, 주문구분)

        if self.dict_jg:
            if gubun == '수동':
                self.teleQ.put('잔고청산 주문을 전송합니다.')
            for 종목코드 in self.dict_jg.copy():
                현재가 = self.dict_jg[종목코드]['현재가']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                if self.dict_set['모의투자']:
                    주문시간 = self._get_str_ymdhms()
                    self._update_chejan_data('매도', 종목코드, 보유수량, 보유수량, 0, 현재가, 현재가, 주문시간, '')
                else:
                    self._check_order(('매도', 종목코드, 현재가, 보유수량, now(), True))
            if self.dict_set['알림소리']:
                self.soundQ.put('잔고청산 주문을 전송하였습니다.')
            self.windowQ.put((ui_num['기본로그'], '시스템 명령 실행 알림 - 잔고청산 주문 완료'))
        elif gubun == '수동':
            self.teleQ.put('현재는 보유종목이 없습니다.')
        self.dict_bool['잔고청산'] = True

    def _convert_order_data(self, data):
        pass

    @error_decorator
    def _update_chejan_data(self, 주문구분, 종목코드, 주문수량, 체결수량, 미체결수량, 체결가격, 주문가격, 주문시간, 주문번호):
        index = self._get_index()
        종목명 = self.dict_info[종목코드]['종목명']

        if 주문구분 == '시드부족':
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

        elif 주문구분 in ('매수', '매도'):
            if 주문구분 == '매수':
                # ['종목명', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간']
                if 종목코드 in self.dict_jg:
                    보유수량 = round(self.dict_jg[종목코드]['보유수량'] + 체결수량, 8)
                    매입금액 = int(self.dict_jg[종목코드]['매입금액'] + 체결수량 * 체결가격)
                    매수가 = round(매입금액 / 보유수량, 4)
                    평가금액, 수익금, 수익률 = get_stock_os_profit(매입금액, 보유수량 * 체결가격)
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
                    매입금액 = int(체결수량 * 체결가격)
                    평가금액, 수익금, 수익률 = get_stock_os_profit(매입금액, 체결수량 * 체결가격)
                    self.dict_jg[종목코드] = {
                        '종목명': 종목명,
                        '매수가': 체결가격,
                        '현재가': 체결가격,
                        '수익률': 수익률,
                        '평가손익': 수익금,
                        '매입금액': 매입금액,
                        '평가금액': 평가금액,
                        '보유수량': 체결수량,
                        '분할매수횟수': 0,
                        '분할매도횟수': 0,
                        '매수시간': 주문시간
                    }

                if 미체결수량 == 0:
                    self.dict_jg[종목코드]['분할매수횟수'] += 1
                    if 종목코드 in self.dict_order[주문구분]:
                        del self.dict_order[주문구분][종목코드]

            else:
                if 종목코드 not in self.dict_jg: return
                매수가 = self.dict_jg[종목코드]['매수가']
                보유수량 = round(self.dict_jg[종목코드]['보유수량'] - 체결수량, 8)
                if 보유수량 != 0:
                    매입금액 = int(매수가 * 보유수량)
                    평가금액, 수익금, 수익률 = get_stock_os_profit(매입금액, 보유수량 * 체결가격)
                    # ['종목명', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간']
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

                매입금액 = 매수가 * 체결수량
                평가금액, 수익금, 수익률 = get_stock_os_profit(매입금액, 체결수량 * 체결가격)
                if -100 < 수익률 < 100: self._update_tradelist(index, 종목명, 매입금액, 평가금액, 체결수량, 수익률, 수익금, 주문시간)
                if 수익률 < 0: self.dict_info[종목코드]['손절거래시간'] = timedelta_sec(self.dict_set['매수금지손절간격초'])

            self.dict_jg = dict(sorted(self.dict_jg.items(), key=lambda x: x[1]['매입금액'], reverse=True))

            if 미체결수량 == 0:
                self._put_order_complete(주문구분 + '완료', 종목코드)
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

            if 주문구분 == '매수':
                self.dict_intg['예수금'] -= 체결수량 * 체결가격
                if self.dict_set['모의투자']:
                    self.dict_intg['추정예수금'] -= 체결수량 * 체결가격
            else:
                self.dict_intg['예수금'] += 매입금액 + 수익금
                self.dict_intg['추정예수금'] += 매입금액 + 수익금

            if self.dict_jg:
                df_jg = pd.DataFrame.from_dict(self.dict_jg, orient='index')
            else:
                df_jg = pd.DataFrame(columns=columns_jg)
            self.queryQ.put(('거래디비', df_jg, 'c_jangolist', 'replace'))
            if self.dict_set['알림소리']: self.soundQ.put(f"{종목코드} {주문구분}하였습니다.")
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 체결] {종목코드} | {체결가격} | {체결수량}'))

        elif 주문구분 in ('매수취소', '매도취소'):
            if 주문구분 == '매수취소':
                self.dict_intg['추정예수금'] += 주문수량 * 주문가격

            if 종목코드 in self.dict_order[주문구분]:
                del self.dict_order[주문구분][종목코드]

            self._put_order_complete(주문구분, 종목코드)
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

            if self.dict_set['알림소리']: self.soundQ.put(f"{종목명} {주문구분}하였습니다.")
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분}] {종목명} | {주문가격} | {주문수량}'))

        self.receivQ.put(('잔고목록', tuple(self.dict_jg)))
        self.receivQ.put(('주문목록', self._get_order_code_list()))
