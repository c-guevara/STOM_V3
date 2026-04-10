
import pandas as pd
from PyQt5.QtCore import QTimer
from trade.base_trader import BaseTrader
from utility.setting_base import ui_num, columns_jgf
from trade.ls_rest_api import LsRestAPI, WebSocketTrader
from utility.static import now, timedelta_sec, get_future_os_long_profit, get_future_os_short_profit, qtest_qwait, \
    error_decorator


class FutureOsTrader(BaseTrader):
    def __init__(self, qlist, dict_set, market_infos):
        super().__init__(qlist, dict_set, market_infos)

        self.dict_order  = {
            'BUY_LONG': {},
            'SELL_LONG': {},
            'SELL_SHORT': {},
            'BUY_SHORT': {}
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
            yesugm = self.ls.get_balance_future_oversea()
        self._set_yesugm_and_noti(yesugm)

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

            """def order_future_oversea(self, 종목코드, 주문구분, 주문가격, 주문수량, 주문유형):"""
            od_no, msg = self.ls.order_future_oversea(종목코드, 주문구분, 주문가격, 주문수량, 주문유형)
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
                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'
                ))
                self.windowQ.put((ui_num['기본로그'], msg))

        elif 주문구분 in ('매수정정', '매도정정'):
            """def order_modify_future_oversea(self, 종목코드, 원주문번호, 주문구분, 주문가격, 주문수량, 주문유형):"""
            주문구분_ = 주문구분[:2]
            주문유형 = self.dict_set[f'{주문구분_}주문유형']
            od_no, msg = self.ls.order_modify_future_oversea(종목코드, 원주문번호, 주문구분_, 주문가격, 주문수량, 주문유형)
            if od_no == '0':
                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'
                ))
                self.windowQ.put((ui_num['기본로그'], msg))

        elif 주문구분 in ('매수취소', '매도취소'):
            """def order_cancel_future_oversea(self, 종목코드, 원주문번호):"""
            od_no, msg = self.ls.order_cancel_future_oversea(종목코드, 원주문번호)
            if od_no == '0':
                self.windowQ.put((
                    ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분} 실패] {종목명} | {주문가격} | {주문수량}'
                ))
                self.windowQ.put((ui_num['기본로그'], msg))

        self.order_time = timedelta_sec(0.2)
        self.receivQ.put(('주문목록', self._get_order_code_list()))

    def _update_Jango(self, data):
        종목코드, 현재가 = data
        self.dict_curc[종목코드] = 현재가
        try:
            """['종목명', '포지션', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량',
                '분할매수횟수', '분할매도횟수', '매수시간']"""
            if 현재가 != self.dict_jg[종목코드]['현재가']:
                포지션 = self.dict_jg[종목코드]['포지션']
                매수가 = self.dict_jg[종목코드]['매수가']
                매입금액 = self.dict_jg[종목코드]['매입금액']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                평가금액 = 매입금액 + (현재가 - 매수가) * self.dict_info[종목코드]['틱가치'] * 보유수량
                if 포지션 == 'LONG':
                    평가금액, 평가손익, 수익률 = get_future_os_long_profit(매입금액, 평가금액)
                else:
                    평가금액, 평가손익, 수익률 = get_future_os_short_profit(매입금액, 평가금액)
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
                현재시간 = now()
                주문번호 = last_value['주문번호']
                self._create_order(f'{주문구분}_CANCEL', 종목코드, 종목명, 0, 미체결수량, 주문번호, 현재시간, False, 0, None)

    def _modify_order(self, 종목코드, 주문구분):
        종목명 = self.dict_info[종목코드]['종목명']
        last_value = self._get_chejan_last_value(종목명, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                if 주문구분 == 'BUY_LONG':
                    정정가격 = self.dict_curc[종목코드] - self.dict_info[종목코드]['호가단위'] * self.dict_set['매수정정호가']
                elif 주문구분 == 'SELL_SHORT':
                    정정가격 = self.dict_curc[종목코드] + self.dict_info[종목코드]['호가단위'] * self.dict_set['매수정정호가']
                elif 주문구분 == 'SELL_LONG':
                    정정가격 = self.dict_curc[종목코드] + self.dict_info[종목코드]['호가단위'] * self.dict_set['매도정정호가']
                else:
                    정정가격 = self.dict_curc[종목코드] - self.dict_info[종목코드]['호가단위'] * self.dict_set['매도정정호가']

                현재시간 = now()
                주문번호 = last_value['주문번호']
                self._create_order(f'{주문구분}_MODIFY', 종목코드, 종목명, 정정가격, 미체결수량, 주문번호, 현재시간, False, 0, None)

    def _jango_cheongsan(self, gubun):
        for 주문구분 in self.dict_order:
            for 종목코드 in self.dict_order[주문구분]:
                self._cancel_order(종목코드, 주문구분)

        if self.dict_jg:
            if gubun == '수동':
                self.teleQ.put('해선 잔고청산 주문을 전송합니다.')
            for 종목코드 in self.dict_jg.copy():
                포지션 = self.dict_jg[종목코드]['포지션']
                종목명 = self.dict_jg[종목코드]['종목명']
                현재가 = self.dict_jg[종목코드]['현재가']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                주문구분 = 'SELL_LONG' if 포지션 == 'LONG' else 'BUY_SHORT'
                if self.dict_set['모의투자']:
                    self.dict_signal[종목코드] = 주문구분
                    주문시간 = self._get_str_ymdhms()
                    self._update_chejan_data('매도', 종목코드, 보유수량, 보유수량, 0, 현재가, 현재가, 주문시간, '')
                else:
                    self._check_order((주문구분, 종목코드, 종목명, 현재가, 보유수량, now(), True))
            if self.dict_set['알림소리']:
                self.windowQ.put(('sound', '해선 잔고청산 주문을 전송하였습니다.'))
            self.windowQ.put((ui_num['기본로그'], f'시스템 명령 실행 알림 - 해선 잔고청산 주문 완료'))
        elif gubun == '수동':
            self.teleQ.put('현재는 해선 보유종목이 없습니다.')
        self.dict_bool['잔고청산'] = True

    def _sys_exit(self):
        qtest_qwait(5)
        self.windowQ.put((ui_num['기본로그'], '시스템 명령 실행 알림 - 트레이더 종료'))

    def _convert_order_data(self, data):
        pass

    @error_decorator
    def _update_chejan_data(self, 주문구분, 종목코드, 주문수량, 체결수량, 미체결수량, 체결가격, 주문가격, 주문시간, 주문번호):
        index = self._get_index()
        종목명 = self.dict_info[종목코드]['종목명']

        gubun = self.dict_signal.get(종목코드, None)
        if gubun is None:
            self.windowQ.put((ui_num['시스템로그'], '오류 알림 - HTS 수동 주문은 포지션 방향을 추적할 수 없어 기록하지 않습니다.'))
            return

        if 주문구분 in ('매수', '매도'):
            if gubun in ('BUY_LONG', 'SELL_SHORT'):
                # ['종목명', '포지션', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간']
                if 종목코드 in self.dict_jg:
                    직전매수가 = self.dict_jg[종목코드]['매수가']
                    직전보유수량 = self.dict_jg[종목코드]['보유수량']
                    직전매입금액 = self.dict_jg[종목코드]['매입금액']
                    보유수량 = 직전보유수량 + 체결수량
                    매입금액 = 직전매입금액 + self.dict_info[종목코드]['위탁증거금'] * 체결수량
                    매수가 = round((직전매수가 * 직전보유수량 + 체결가격 * 체결수량) / 보유수량, self.dict_info[종목코드]['소숫점자리수'] + 1)
                    평가금액 = 매입금액 + (체결가격 - 매수가) * self.dict_info[종목코드]['틱가치'] * 보유수량
                    if 'LONG' in gubun:
                        평가금액, 수익금, 수익률 = get_future_os_long_profit(매입금액, 평가금액)
                    else:
                        평가금액, 수익금, 수익률 = get_future_os_short_profit(매입금액, 평가금액)
                    self.dict_jg[종목코드].update({
                        '매수가': 매수가,
                        '현재가': 체결가격,
                        '수익률': 수익률,
                        '평가손익': 수익금,
                        '매입금액': 매입금액,
                        '평가금액': 평가금액,
                        '보유수량': 보유수량,
                        '매수시간': index[:14]
                    })
                else:
                    보유수량 = 체결수량
                    매입금액 = 평가금액 = self.dict_info[종목코드]['위탁증거금'] * 체결수량
                    if 'LONG' in gubun:
                        포지션 = 'LONG'
                        평가금액, 수익금, 수익률 = get_future_os_long_profit(매입금액, 평가금액)
                    else:
                        포지션 = 'SHORT'
                        평가금액, 수익금, 수익률 = get_future_os_short_profit(매입금액, 평가금액)
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
                        '매수시간': index[:14]
                    }

                if 미체결수량 == 0:
                    if 보유수량 > 0:
                        self.dict_jg[종목코드]['분할매수횟수'] += 1
                    if 종목코드 in self.dict_order[gubun]:
                        del self.dict_order[gubun][종목코드]

            else:
                if 종목코드 not in self.dict_jg: return
                포지션 = self.dict_jg[종목코드]['포지션']
                매수가 = self.dict_jg[종목코드]['매수가']
                보유수량 = self.dict_jg[종목코드]['보유수량'] - 체결수량
                if 보유수량 != 0:
                    매입금액 = self.dict_info[종목코드]['위탁증거금'] * 보유수량
                    평가금액 = 매입금액 + (체결가격 - 매수가) * self.dict_info[종목코드]['틱가치'] * 보유수량
                    if 'LONG' in gubun:
                        평가금액, 수익금, 수익률 = get_future_os_long_profit(매입금액, 평가금액)
                    else:
                        평가금액, 수익금, 수익률 = get_future_os_short_profit(매입금액, 평가금액)
                    # ['종목명', '포지션', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간', '레버리지']
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
                    if 종목코드 in self.dict_order[gubun]:
                        del self.dict_order[gubun][종목코드]

                매입금액 = self.dict_info[종목코드]['위탁증거금'] * 체결수량
                평가금액 = 매입금액 + (체결가격 - 매수가) * self.dict_info[종목코드]['틱가치'] * 체결수량
                if 'LONG' in gubun:
                    평가금액, 수익금, 수익률 = get_future_os_long_profit(매입금액, 평가금액)
                else:
                    평가금액, 수익금, 수익률 = get_future_os_short_profit(매입금액, 평가금액)
                if -100 < 수익률 < 100: self._update_tradelist(index, 종목명, 포지션, 매입금액, 평가금액, 체결수량, 수익률, 수익금, 주문시간)
                if 수익률 < 0: self.dict_info[종목코드]['손절거래시간'] = timedelta_sec(self.dict_set['매수금지손절간격초'])

            self.dict_jg = dict(sorted(self.dict_jg.items(), key=lambda x: x[1]['매입금액'], reverse=True))

            if 미체결수량 == 0:
                self._put_order_complete(f'{gubun}_COMPLETE', 종목코드)
            self._update_chegeollist(index, 종목코드, 종목명, gubun, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

            총위탁증거금 = 체결수량 * self.dict_info[종목코드]['위탁증거금']
            if gubun in ('BUY_LONG', 'SELL_SHORT'):
                self.dict_intg['예수금'] -= 총위탁증거금
                if self.dict_set['모의투자']:
                    self.dict_intg['추정예수금'] -= 총위탁증거금
            else:
                self.dict_intg['추정예탁자산'] += 수익금
                self.dict_intg['예수금'] += 총위탁증거금 + 수익금
                self.dict_intg['추정예수금'] += 총위탁증거금 + 수익금

            if self.dict_jg:
                df_jg = pd.DataFrame.from_dict(self.dict_jg, orient='index')
            else:
                df_jg = pd.DataFrame(columns=columns_jgf)
            self.queryQ.put(('거래디비', df_jg, 'f_jangolist', 'replace'))
            if self.dict_set['알림소리']: self.windowQ.put(('sound', f'{종목명} {체결수량}주를 {주문구분}하였습니다'))
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{gubun}] {종목명} | {체결가격} | {체결수량}'))

        elif 주문구분 == '시드부족':
            self._update_chegeollist(index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

        elif 주문구분 in ('정정', '취소'):
            if 주문구분 == '정정':
                gubun_ = gubun.replace('_MODIFY', '')
                정정횟수 = self.dict_order[gubun_][종목코드][1] + 1
                취소시간 = timedelta_sec(self.dict_set['매수취소시간초' if gubun in ('BUY_LONG', 'SELL_SHORT') else '매도취소시간초'])
                self.dict_order[gubun_][종목코드] = [취소시간, 정정횟수, 주문가격]
            else:
                gubun_ = gubun.replace('_CANCEL', '')
                if gubun in ('BUY_LONG', 'SELL_SHORT'):
                    self.dict_intg['추정예수금'] += 주문수량 * self.dict_info[종목코드]['위탁증거금']

                if 종목코드 in self.dict_order[gubun_]:
                    del self.dict_order[gubun_][종목코드]

                self._put_order_complete(gubun, 종목코드)

            self._update_chegeollist(index, 종목코드, 종목명, gubun, 주문수량, 체결수량, 미체결수량, 체결가격, 주문시간, 주문가격, 주문번호)

            if self.dict_set['알림소리']: self.windowQ.put(('sound', f'{종목명} {주문수량}주를 {주문구분}하였습니다'))
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{gubun}] {종목명} | {주문가격} | {주문수량}'))

        elif 주문구분 in ('미접수', '취소', '거부'):
            self.windowQ.put((ui_num['기본로그'], f'주문 관리 시스템 알림 - [{주문구분}] {종목명} | {주문가격} | {주문수량}'))

        self.receivQ.put(('잔고목록', tuple(self.dict_jg)))
        self.receivQ.put(('주문목록', self._get_order_code_list()))
