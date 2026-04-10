
import pandas as pd
from PyQt5.QtCore import QTimer
from trade.base_trader import BaseTrader
from utility.setting_base import ui_num,  columns_jg
from trade.upbit.upbit_restapi import Upbit, WebSocketTrader
from utility.static import now, timedelta_sec, qtest_qwait, error_decorator, get_upbit_hoga_unit, get_upbit_profit


class UpbitTrader(BaseTrader):
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

        self.upbit = Upbit(access_key, secret_key)

        if not self.dict_set['모의투자']:
            self.ws_thread = WebSocketTrader(self.windowQ)
            self.ws_thread.signal.connect(self._convert_order_data)
            self.ws_thread.start()

        self._get_balances()

    def _get_balances(self):
        if self.dict_set['모의투자']:
            yesugm = self._get_yesugm_for_paper_trading()
        else:
            yesugm = self.upbit.get_balances()
        self._set_yesugm_and_noti(yesugm)

    def _check_error(self, ret):
        if ret.__class__ == dict and list(ret)[0] == 'error':
            self.windowQ.put((ui_num['시스템로그'], f"오류 알림 - {ret['error']['name']} : {ret['error']['message']}"))
            return False
        return True

    def _send_order(self, data):
        curr_time = now()
        if curr_time < self.order_time:
            next_time = (self.order_time - curr_time).total_seconds()
            QTimer.singleShot(int(next_time * 1000), lambda: self._send_order(data))
            return

        주문구분, 종목코드, 종목명, 주문가격, 주문수량, 원주문번호, 시그널시간, 잔고청산, 정정횟수, 수동주문유형 = data
        self._order_time_log(시그널시간)

        if 주문구분 in ('매수', '매도'):
            if 잔고청산:
                주문유형 = '시장가'
            else:
                주문유형 = self.dict_set[f'{주문구분}주문유형'] if 수동주문유형 is None else 수동주문유형
            주문금액 = int(주문가격 * 주문수량)

            """def order_coin(self, 종목코드='', 주문구분코드='', 주문유형='', 주문금액=0, 주문수량=0):"""
            ret = self.upbit.order_coin(종목코드=종목코드, 주문구분=주문구분, 주문유형=주문유형, 주문금액=주문금액, 주문수량=주문수량)
            if ret is not None:
                if self._check_error(ret):
                    index = self._get_index()
                    if 주문구분 == '매수':
                        self.dict_intg['추정예수금'] -= 주문수량 * 주문가격
                        add_time = self.dict_set['매수취소시간초']
                    else:
                        add_time = self.dict_set['매도취소시간초']

                    # noinspection PyUnresolvedReferences
                    self.dict_order[주문구분][종목코드] = [
                        timedelta_sec(add_time), 정정횟수, 주문가격, get_upbit_hoga_unit(주문가격)
                    ]

                    # noinspection PyUnresolvedReferences
                    self._update_chegeollist(
                        index, 종목코드, 종목명, f'{주문구분} 접수', 주문수량, 0, 주문수량, 0, index[:14], 주문가격, ret['uuid']
                    )

                    self.windowQ.put((
                        ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 접수] {종목명} | {주문가격} | {주문수량}'
                    ))
            else:
                self._put_order_complete(f'{주문구분}취소', 종목코드)
                self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'))

        elif 주문구분 in ('매수취소', '매도취소'):
            """def order_cancel(self, od_no):"""
            ret = self.upbit.order_cancel(원주문번호)
            if ret is None:
                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'
                ))

        self.order_time = timedelta_sec(0.2)
        self.receivQ.put(('주문목록', self._get_order_code_list()))

    def _check_chegeol(self):
        order_info_list = []
        for gubun in self.dict_order:
            for code, orders in self.dict_order[gubun].items():
                order_info = self._get_order_Info(code, orders[0])
                if order_info is not None:
                    order_info_list.append([gubun] + order_info)
                qtest_qwait(0.1)

        if order_info_list:
            for 주문구분, 종목코드, 주문수량, 총체결수량, 미체결수량, 체결가격, 주문가격, 주문번호 in order_info_list:
                체결시간 = self._get_str_ymdhms()
                self._update_chejan_data(주문구분, 종목코드, 주문수량, 총체결수량, 미체결수량, 체결가격, 주문가격, 체결시간, 주문번호)

    def _get_order_Info(self, 종목코드, 주문번호):
        order_info = None
        ret = self.upbit.get_order_info(주문번호)
        if ret is not None and self._check_error(ret):
            try:
                주문가격 = float(ret['price'])
            except:
                주문가격 = 0.
            try:
                주문수량 = float(ret['volume'])
            except:
                주문수량 = 0.
            try:
                미체결수량 = float(ret['remaining_volume'])
            except:
                미체결수량 = 0.

            총체결수량, 체결가격, 매입금액 = 0., 0., 0.
            if ret['trades_count'] > 0:
                trades = ret['trades']
                for i in range(len(trades)):
                    매입금액 += float(trades[i]['funds'])
                    총체결수량 += float(trades[i]['volume'])
                if 총체결수량 > 0:
                    체결가격 = round(매입금액 / 총체결수량, 4)
                    총체결수량 = round(총체결수량, 8)

            if 총체결수량 > 0:
                if 주문번호 not in self.dict_order_cc:
                    order_info = [종목코드, 주문수량, 총체결수량, 미체결수량, 체결가격, 주문가격, 주문번호]
                else:
                    체결수량 = round(총체결수량 - self.dict_order_cc[주문번호], 8)
                    if 체결수량 > 0:
                        order_info = [종목코드, 주문수량, 체결수량, 미체결수량, 체결가격, 주문가격, 주문번호]

                self.dict_order_cc[주문번호] = 총체결수량
                if 미체결수량 == 0 and 주문번호 in self.dict_order_cc:
                    del self.dict_order_cc[주문번호]

        return order_info

    def _update_Jango(self, data):
        종목코드, 현재가 = data
        self.dict_curc[종목코드] = 현재가
        try:
            """['종목명', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량',
                '분할매수횟수', '분할매도횟수', '매수시간']"""
            if 현재가 != self.dict_jg[종목코드]['현재가']:
                매입금액 = self.dict_jg[종목코드]['매입금액']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                평가금액, 평가손익, 수익률 = get_upbit_profit(매입금액, 보유수량 * 현재가)
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
        last_value = self._get_chejan_last_value(종목코드, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                주문번호, 주문가격 = last_value['주문번호'], last_value['주문가격']
                self._create_order(f'{주문구분}취소', 종목코드, 종목명, 주문가격, 미체결수량, 주문번호, now(), False, 0, None)

    def _modify_order(self, 종목코드, 주문구분):
        종목명 = self.dict_info[종목코드]['종목명']
        last_value = self._get_chejan_last_value(종목코드, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                if 주문구분 == '매수':
                    정정가격 = self.dict_curc[종목코드] - self.dict_order[주문구분][종목코드][3] * self.dict_set['매수정정호가']
                else:
                    정정가격 = self.dict_curc[종목코드] + self.dict_order[주문구분][종목코드][3] * self.dict_set['매도정정호가']

                현재시간 = now()
                정정횟수 = self.dict_order[주문구분][종목코드][1] + 1
                주문번호, 주문가격 = last_value['주문번호'], last_value['주문가격']
                self._create_order(f'{주문구분}취소', 종목코드, 종목명, 주문가격, 미체결수량, 주문번호, 현재시간, False, 0, None)
                self._create_order(주문구분, 종목코드, 종목명, 정정가격, 미체결수량, '', 현재시간, False, 정정횟수, None)

    def _jango_cheongsan(self, gubun):
        for 주문구분 in self.dict_order:
            if 주문구분 in ('매수', '매도'):
                for 종목코드 in self.dict_order[주문구분]:
                    self._cancel_order(종목코드, 주문구분)

        if self.dict_jg:
            if gubun == '수동':
                self.teleQ.put('잔고청산 주문을 전송합니다.')
            for 종목코드 in self.dict_jg.copy():
                종목명 = self.dict_jg[종목코드]['종목명']
                현재가 = self.dict_jg[종목코드]['현재가']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                if self.dict_set['모의투자']:
                    주문시간 = self._get_str_ymdhms()
                    self._update_chejan_data('매도', 종목코드, 보유수량, 보유수량, 0, 현재가, 현재가, 주문시간, '')
                else:
                    self._check_order(('매도', 종목코드, 종목명, 현재가, 보유수량, now(), True))
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

        if 주문구분 in ('매수', '매도'):
            if 주문구분 == '매수':
                """['종목명', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량',
                    '분할매수횟수', '분할매도횟수', '매수시간']"""
                if 종목코드 in self.dict_jg:
                    보유수량 = round(self.dict_jg[종목코드]['보유수량'] + 체결수량, 8)
                    매입금액 = int(self.dict_jg[종목코드]['매입금액'] + 체결수량 * 체결가격)
                    매수가 = round(매입금액 / 보유수량, 4)
                    평가금액, 수익금, 수익률 = get_upbit_profit(매입금액, 보유수량 * 체결가격)
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
                    평가금액, 수익금, 수익률 = get_upbit_profit(매입금액, 체결수량 * 체결가격)
                    self.dict_jg[종목코드] = {
                        '종목명': 종목코드,
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
                    평가금액, 수익금, 수익률 = get_upbit_profit(매입금액, 보유수량 * 체결가격)
                    """['종목명', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량',
                        '분할매수횟수', '분할매도횟수', '매수시간']"""
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
                평가금액, 수익금, 수익률 = get_upbit_profit(매입금액, 체결수량 * 체결가격)
                if -100 < 수익률 < 100:
                    self._update_tradelist(index, 종목코드, 종목명, 매입금액, 평가금액, 체결수량, 수익률, 수익금, 주문시간)
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

        elif 주문구분 == '시드부족':
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

        elif 주문구분 in ('매수취소', '매도취소'):
            if 주문구분 == '매수취소':
                self.dict_intg['추정예수금'] += 주문수량 * 주문가격

            if 종목코드 in self.dict_order[주문구분]:
                del self.dict_order[주문구분][종목코드]

            self._put_order_complete(주문구분, 종목코드)
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

            if self.dict_set['알림소리']: self.soundQ.put(f"{종목코드} {주문구분}하였습니다.")
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분}] {종목코드} | {주문가격} | {주문수량}'))

        self.receivQ.put(('잔고목록', tuple(self.dict_jg)))
        self.receivQ.put(('주문목록', self._get_order_code_list()))
