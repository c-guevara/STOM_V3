
import sqlite3
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from utility.setting_base import columns_cj, ui_num, DB_TRADELIST, columns_jg, columns_td, columns_tdf
from utility.static import now, now_cme, now_utc, str_hmsf, str_ymdhms, str_ymdhmsf, str_hms, str_ymd, dt_hms, \
    timedelta_sec, error_decorator, get_hogaunit_stock, get_hogaunit_coin, set_builtin_print, get_profit_stock, \
    get_profit_stock_os, get_profit_coin, get_profit_future_long, get_profit_future_os_long, \
    get_profit_coin_future_long, get_profit_future_short, get_profit_future_os_short, get_profit_coin_future_short


class MonitorTraderQ(QThread):
    signal1 = pyqtSignal(tuple)
    signal2 = pyqtSignal(tuple)
    signal3 = pyqtSignal(tuple)
    signal4 = pyqtSignal(str)

    def __init__(self, traderQ, market_gubun):
        super().__init__()
        self.traderQ = traderQ
        self.market_gubun = market_gubun

    def run(self):
        while True:
            data = self.traderQ.get()
            if data.__class__ == tuple:
                if len(data) in (7, 8):
                    if self.market_gubun < 6:
                        self.signal1.emit(data)
                    else:
                        self.signal2.emit(data)
                else:
                    self.signal3.emit(data)
            elif data.__class__ == str:
                self.signal4.emit(data)


class BaseTrader:
    def __init__(self, qlist, dict_set, market_infos):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, receivQ, traderQ, stgQs, liveQ
           0        1       2      3       4      5      6      7       8        9       10     11
        """
        self.windowQ      = qlist[0]
        self.soundQ       = qlist[1]
        self.queryQ       = qlist[2]
        self.teleQ        = qlist[3]
        self.receivQ      = qlist[8]
        self.traderQ      = qlist[9]
        self.stgQs        = qlist[10]
        self.stgQ         = qlist[10][0]
        self.liveQ        = qlist[11]
        self.dict_set     = dict_set
        self.market_gubun = market_infos[0]
        self.market_info  = market_infos[1]

        self.dict_cj: dict[str, dict[str, int | float]] = {}  # 체결목록
        self.dict_jg: dict[str, dict[str, int | float]] = {}  # 잔고목록
        self.dict_td: dict[str, dict[str, int | float]] = {}  # 거래목록
        self.dict_signal: dict[str, str] = {}

        self.dict_tj       = {}  # 잔고평가
        self.dict_tt       = {}  # 평가손익
        self.dict_info     = {}
        self.dict_curc     = {}
        self.dict_lvrg     = {}
        self.dict_pos      = {}
        self.dict_sgbn     = {}
        self.dict_order    = {}
        self.dict_order_cc = {}
        self.dict_intg = {
            '예수금': 0,
            '추정예수금': 0,
            '추정예탁자산': 0,
            '종목당투자금': 0
        }
        self.dict_bool = {
            '잔고청산': False
        }

        self.ls         = None
        self.token      = None
        self.upbit      = None
        self.binance    = None
        self.ws_thread  = None

        self.is_tick    = self.dict_set['타임프레임']
        acc_no          = self.market_info['계정번호']
        self.access_key = self.dict_set[f"access_key{acc_no}"]
        self.secret_key = self.dict_set[f"secret_key{acc_no}"]

        self.str_today  = str_ymd()
        self.order_time = now()
        self.jgcs_time  = self.get_jgcs_time()

        self._load_database()
        set_builtin_print(self.windowQ)

    def _get_yesugm_for_paper_trading(self):
        con = sqlite3.connect(DB_TRADELIST)
        df = pd.read_sql(f"SELECT * FROM {self.market_info['거래디비']}", con)
        con.close()
        tcg = df['수익금'].sum()
        yesugm = 100_000_000 + tcg
        if yesugm < 100_000_000:
            yesugm = 100_000_000
        return yesugm

    def _set_yesugm_and_noti(self, yesugm):
        총매입금액 = sum([v['매입금액'] for v in self.dict_jg.values()]) if self.dict_jg else 0
        self.dict_intg['예수금'] = int(yesugm - 총매입금액)
        self.dict_intg['추정예수금'] = int(yesugm - 총매입금액)
        self.dict_intg['추정예탁자산'] = yesugm

        self.windowQ.put((ui_num['기본로그'], f"시스템 명령 실행 알림 - {self.market_info['마켓이름']} 예수금 조회 완료"))
        self.windowQ.put((ui_num['기본로그'], f"시스템 명령 실행 알림 - {self.market_info['마켓이름']} 트레이더 시작"))

    def get_jgcs_time(self):
        return int(str_hms(timedelta_sec(-120, dt_hms(str(self.dict_set['전략종료시간'])))))

    def _load_database(self):
        con = sqlite3.connect(DB_TRADELIST)
        df_cj = pd.read_sql(f"SELECT * FROM {self.market_info['체결디비']} WHERE 체결시간 LIKE '{self.str_today}%'", con)
        df_td = pd.read_sql(f"SELECT * FROM {self.market_info['거래디비']} WHERE 체결시간 LIKE '{self.str_today}%'", con)
        df_cj.set_index('index')
        df_td.set_index('index')
        if len(df_cj) > 0:
            self.dict_cj = df_cj.to_dict('index')
            self.windowQ.put((ui_num['체결목록'], df_cj[::-1]))
        if len(df_td) > 0:
            self.dict_td = df_td.to_dict('index')
            self.windowQ.put((ui_num['거래목록'], df_td[::-1]))
        if self.dict_set['모의투자']:
            df_jg = pd.read_sql(f"SELECT * FROM {self.market_info['잔고디비']}", con).set_index('index')
            if len(df_jg) > 0:
                self.dict_jg = df_jg.to_dict('index')
                self.receivQ.put(('잔고목록', tuple(self.dict_jg)))
        con.close()
        self.windowQ.put((ui_num['기본로그'], f"시스템 명령 실행 알림 - {self.market_info['마켓이름']} 데이터베이스 불러오기 완료"))

    def _scheduler1(self):
        data = ('잔고목록', self.dict_jg.copy())
        if self.market_gubun < 5:
            for q in self.stgQs:
                q.put(data)
        else:
            self.stgQ.put(data)

    def _scheduler2(self):
        inthms = self._get_inthms()
        if self.is_tick and inthms < self.dict_set['전략종료시간']:
            self._order_time_control()

        if self.dict_set['잔고청산'] and not self.dict_bool['잔고청산'] and self.jgcs_time < inthms < self.jgcs_time + 10:
            self._jango_cheongsan('자동')

        self._update_totaljango()

    def _get_inthms(self):
        if self.market_gubun < 4 or self.market_gubun in (6, 7):
            return int(str_hms())
        elif self.market_gubun in (4, 8):
            return int(str_hms(now_cme()))
        else:
            return int(str_hms(now_utc()))

    def _get_str_ymdhms(self):
        if self.market_gubun < 4 or self.market_gubun in (6, 7):
            return str_ymdhms()
        elif self.market_gubun in (4, 8):
            return str_ymdhms(now_cme())
        else:
            return str_ymdhms(now_utc())

    @error_decorator
    def _check_order(self, data):
        if len(data) == 7:
            주문구분, 종목코드, 종목명, 주문가격, 주문수량, 시그널시간, 잔고청산 = data
            수동주문유형 = None
        else:
            주문구분, 종목코드, 종목명, 주문가격, 주문수량, 시그널시간, 잔고청산, 수동주문유형 = data

        잔고없음 = 종목코드 not in self.dict_jg
        매수주문중 = 종목코드 in self.dict_order['매수']
        매도주문중 = 종목코드 in self.dict_order['매도']

        원주문번호 = ''
        주문취소 = False
        현재시간 = now()
        if 잔고청산:
            if 잔고없음 or 매도주문중:
                주문취소 = True
        elif self.dict_bool['잔고청산']:
            주문취소 = True
        elif 주문구분 == '매수':
            inthms = self._get_inthms()
            거래횟수 = len(set([v['체결시간'] for v in self.dict_td.values() if v['종목명'] == 종목명]))
            손절횟수 = len(set([v['체결시간'] for v in self.dict_td.values() if v['종목명'] == 종목명 and v['수익률'] < 0]))
            if self.dict_set['매수금지거래횟수'] and self.dict_set['매수금지거래횟수값'] <= 거래횟수:
                주문취소 = True
            elif self.dict_set['매수금지손절횟수'] and self.dict_set['매수금지손절횟수값'] <= 손절횟수:
                주문취소 = True
            elif 잔고없음 and inthms < self.dict_set['전략종료시간'] and len(self.dict_jg) >= self.dict_set['최대매수종목수']:
                주문취소 = True
            elif self.dict_set['매수금지간격'] and 현재시간 < self.dict_info[종목코드]['최종거래시간']:
                주문취소 = True
            elif self.dict_set['매수금지손절간격'] and 현재시간 < self.dict_info[종목코드]['손절거래시간']:
                주문취소 = True
            elif not 잔고없음 and self.dict_jg[종목코드]['분할매수횟수'] >= self.dict_set['매수분할횟수']:
                주문취소 = True
            elif self.dict_intg['추정예수금'] < 주문수량 * 주문가격:
                if 현재시간 > self.dict_info[종목코드]['시드부족시간']:
                    self._create_order('시드부족', 종목코드, 종목명, 주문가격, 주문수량, '', 시그널시간, 잔고청산, 0, None)
                    self.dict_info[종목코드]['시드부족시간'] = timedelta_sec(180)
                주문취소 = True
            elif 매수주문중:
                주문취소 = True
        elif 주문구분 == '매도':
            if 잔고없음 or 매도주문중:
                주문취소 = True
            elif self.dict_set['매도금지간격'] and 현재시간 < self.dict_info[종목코드]['최종거래시간']:
                주문취소 = True
        elif '취소' in 주문구분:
            if 주문구분 == '매수취소' and not 매수주문중:
                주문취소 = True
            elif 주문구분 == '매도취소' and not 매도주문중:
                주문취소 = True

        if 주문취소:
            if '취소' not in 주문구분:
                self._put_order_complete(f'{주문구분}취소', 종목코드)
        else:
            if 주문수량 > 0:
                if 잔고청산: self._put_order_complete(f'{주문구분}주문', 종목코드)
                self._create_order(주문구분, 종목코드, 종목명, 주문가격, 주문수량, 원주문번호, 시그널시간, 잔고청산, 0, 수동주문유형)
            else:
                if 주문구분 == '매수':
                    if self.dict_set['매도취소매수시그널'] and 매도주문중: self._cancel_order(종목코드, 주문구분)
                elif 주문구분 == '매도':
                    if self.dict_set['매수취소매도시그널'] and 매수주문중: self._cancel_order(종목코드, 주문구분)
                self._put_order_complete(f'{주문구분}취소', 종목코드)

    @error_decorator
    def _check_order_future(self, data):
        if len(data) == 7:
            주문구분, 종목코드, 종목명, 주문가격, 주문수량, 시그널시간, 잔고청산 = data
            수동주문유형 = None
        else:
            주문구분, 종목코드, 종목명, 주문가격, 주문수량, 시그널시간, 잔고청산, 수동주문유형 = data

        잔고없음 = 종목코드 not in self.dict_jg
        롱매수주문중 = 종목코드 in self.dict_order['BUY_LONG']
        숏매수주문중 = 종목코드 in self.dict_order['SELL_SHORT']
        롱매도주문중 = 종목코드 in self.dict_order['SELL_LONG']
        숏매도주문중 = 종목코드 in self.dict_order['BUY_SHORT']
        jg_data = self.dict_jg.get(종목코드)
        포지션 = jg_data['포지션'] if jg_data else None

        원주문번호 = ''
        주문취소 = False
        현재시간 = now()
        if 잔고청산:
            if 잔고없음 or (주문구분 == 'SELL_LONG' and 롱매도주문중) or (주문구분 == 'BUY_SHORT' and 숏매도주문중):
                주문취소 = True
        elif self.dict_bool['잔고청산']:
            주문취소 = True
        elif 주문구분 in ('BUY_LONG', 'SELL_SHORT'):
            inthmsutc = int(str_hms(now_utc()))
            거래횟수 = len(set([v['체결시간'] for v in self.dict_td.values() if v['종목명'] == 종목코드]))
            손절횟수 = len(set([v['체결시간'] for v in self.dict_td.values() if v['종목명'] == 종목코드 and v['수익률'] < 0]))
            if self.dict_set['매수금지거래횟수'] and self.dict_set['매수금지거래횟수값'] <= 거래횟수:
                주문취소 = True
            elif self.dict_set['매수금지손절횟수'] and self.dict_set['매수금지손절횟수값'] <= 손절횟수:
                주문취소 = True
            elif 잔고없음 and inthmsutc < self.dict_set['전략종료시간'] and len(self.dict_jg) >= self.dict_set['최대매수종목수']:
                주문취소 = True
            elif self.dict_set['매수금지간격'] and 현재시간 < self.dict_info[종목코드]['최종거래시간']:
                주문취소 = True
            elif self.dict_set['매수금지손절간격'] and 현재시간 < self.dict_info[종목코드]['손절거래시간']:
                주문취소 = True
            elif not 잔고없음 and self.dict_jg[종목코드]['분할매수횟수'] >= self.dict_set['매수분할횟수']:
                주문취소 = True
            elif self.dict_intg['추정예수금'] < 주문수량 * 주문가격:
                if 현재시간 > self.dict_info[종목코드]['시드부족시간']:
                    self._create_order('시드부족', 종목코드, 종목코드, 주문가격, 주문수량, str_hmsf(), 시그널시간, 잔고청산, 0, None)
                    self.dict_info[종목코드]['시드부족시간'] = timedelta_sec(180)
                주문취소 = True
            elif 포지션 == 'LONG' and 'SHORT' in 주문구분: 주문취소 = True
            elif 포지션 == 'SHORT' and 'LONG' in 주문구분: 주문취소 = True
            elif 주문구분 == 'BUY_LONG' and 롱매수주문중:   주문취소 = True
            elif 주문구분 == 'SELL_SHORT' and 숏매수주문중: 주문취소 = True
        elif 주문구분 in ('SELL_LONG', 'BUY_SHORT'):
            if 포지션 == 'LONG' and 'SHORT' in 주문구분:   주문취소 = True
            elif 포지션 == 'SHORT' and 'LONG' in 주문구분: 주문취소 = True
            elif 주문구분 == 'SELL_LONG' and 롱매도주문중:  주문취소 = True
            elif 주문구분 == 'BUY_SHORT' and 숏매도주문중:  주문취소 = True
            elif self.dict_set['매도금지간격'] and 현재시간 < self.dict_info[종목코드]['최종거래시간']:
                주문취소 = True
        elif 'CANCEL' in 주문구분:
            if 주문구분 == 'BUY_LONG_CANCEL' and not 롱매수주문중:     주문취소 = True
            elif 주문구분 == 'SELL_SHORT_CANCEL' and not 숏매수주문중: 주문취소 = True
            elif 주문구분 == 'SELL_LONG_CANCEL' and not 롱매도주문중:  주문취소 = True
            elif 주문구분 == 'BUY_SHORT_CANCEL' and not 숏매도주문중:  주문취소 = True

        if 주문취소:
            if 'CANCEL' not in 주문구분:
                self._put_order_complete(f'{주문구분}_CANCEL', 종목코드)
        else:
            if 주문수량 > 0:
                if 잔고청산:
                    self._put_order_complete(f'{주문구분}_MANUAL', 종목코드)
                self._create_order(주문구분, 종목코드, 종목명, 주문가격, 주문수량, 원주문번호, 시그널시간, 잔고청산, 0, 수동주문유형)
            else:
                if 주문구분 == 'BUY_LONG':
                    if self.dict_set['매도취소매수시그널'] and 롱매도주문중: self._cancel_order(종목코드, 주문구분)
                elif 주문구분 == 'SELL_SHORT':
                    if self.dict_set['매도취소매수시그널'] and 숏매도주문중: self._cancel_order(종목코드, 주문구분)
                elif 주문구분 == 'SELL_LONG':
                    if self.dict_set['매수취소매도시그널'] and 롱매수주문중: self._cancel_order(종목코드, 주문구분)
                elif 주문구분 == 'BUY_SHORT':
                    if self.dict_set['매수취소매도시그널'] and 숏매수주문중: self._cancel_order(종목코드, 주문구분)
                self._put_order_complete(f'{주문구분}_CANCEL', 종목코드)

    def _put_order_complete(self, 주문구분, 종목코드):
        data = (주문구분, 종목코드)
        if self.market_gubun < 5:
            self.stgQs[self.dict_sgbn[종목코드]].put(data)
        else:
            self.stgQ.put(data)

    def _create_order(self, 주문구분, 종목코드, 종목명, 주문가격, 주문수량, 원주문번호, 시그널시간, 잔고청산, 정정횟수, 수동주문유형):
        if self.market_gubun < 6:
            if 주문구분 == '매수' and 정정횟수 == 0:
                if 수동주문유형 is None and '지정가' in self.dict_set['매수주문유형']:
                    주문가격 = self._get_order_buy_price(종목코드, 주문구분, 주문가격)
            elif 주문구분 == '매도' and 정정횟수 == 0:
                if 수동주문유형 is None and '지정가' in self.dict_set['매도주문유형']:
                    주문가격 = self._get_order_sell_price(종목코드, 주문구분, 주문가격)
        else:
            if 주문구분 in ('BUY_LONG', 'SELL_SHORT') and 정정횟수 == 0:
                if 수동주문유형 is None and '지정가' in self.dict_set['매수주문유형']:
                    주문가격 = self._get_order_buy_price(종목코드, 주문구분, 주문가격)

            elif 주문구분 in ('SELL_LONG', 'BUY_SHORT') and 정정횟수 == 0:
                if 수동주문유형 is None and '지정가' in self.dict_set['매도주문유형']:
                    주문가격 = self._get_order_sell_price(종목코드, 주문구분, 주문가격)

        if self.market_gubun in (6, 7, 8):
            self.dict_signal[종목코드] = 주문구분

        if self.market_gubun == 5 and 주문수량 * 주문가격 < 5000:
            self.windowQ.put((ui_num['시스템로그'], f'오류 알림 - 주문금액이 5천원미만입니다.'))
            self._put_order_complete(f'{주문구분}취소', 종목코드)
            return

        if self.market_gubun == 9 and 주문구분 in ('BUY_LONG', 'SELL_SHORT'):
            주문수량 = round(주문수량 * self.dict_lvrg[종목코드], self.dict_info[종목코드]['수량소숫점자리수'])

        if self.dict_set['모의투자'] or 주문구분 == '시드부족':
            self._order_time_log(시그널시간)
            주문시간 = self._get_str_ymdhms()
            if 주문구분 == '시드부족':
                self._update_chejan_data(주문구분, 종목코드, 주문수량, 0, 주문수량, 주문가격, 0, 주문시간, 원주문번호)
            else:
                if self.market_gubun == 9:
                    self.dict_order[주문구분][종목코드] = [
                        timedelta_sec(self.dict_set['매수취소시간초']), 정정횟수, 주문가격, self.dict_lvrg[종목코드]
                    ]
                else:
                    self.dict_order[주문구분][종목코드] = [
                        timedelta_sec(self.dict_set['매수취소시간초']), 정정횟수, 주문가격
                    ]
                self._update_chejan_data(주문구분, 종목코드, 주문수량, 주문수량, 0, 주문가격, 주문가격, 주문시간, 원주문번호)
        else:
            data = (주문구분, 종목코드, 종목명, 주문가격, 주문수량, 원주문번호, 시그널시간, 잔고청산, 정정횟수, 수동주문유형)
            self._send_order(data)

    def _get_order_buy_price(self, 종목코드, 주문구분, 주문가격):
        매수지정가호가번호 = self.dict_set['매수지정가호가번호']
        if self.market_gubun < 4:
            return int(주문가격 + get_hogaunit_stock(주문가격) * 매수지정가호가번호)
        elif self.market_gubun == 4:
            return round(주문가격 + 0.01 * 매수지정가호가번호, 2)
        elif self.market_gubun == 5:
            return round(주문가격 + get_hogaunit_coin(주문가격) * 매수지정가호가번호, 8)
        elif self.market_gubun in (6, 7, 8):
            소숫점자리수 = self.dict_info[종목코드]['소숫점자리수']
            호가차이 = self.dict_info[종목코드]['호가단위'] * 매수지정가호가번호
            return round(주문가격 + 호가차이, 소숫점자리수) if 주문구분 == 'BUY_LONG' else round(주문가격 - 호가차이, 소숫점자리수)
        else:
            소숫점자리수 = self.dict_info[종목코드]['가격소숫점자리수']
            호가차이 = self.dict_info[종목코드]['호가단위'] * 매수지정가호가번호
            return round(주문가격 + 호가차이, 소숫점자리수) if 주문구분 == 'BUY_LONG' else round(주문가격 - 호가차이, 소숫점자리수)

    def _get_order_sell_price(self, 종목코드, 주문구분, 주문가격):
        매도지정가호가번호 = self.dict_set['매도지정가호가번호']
        if self.market_gubun < 4:
            return int(주문가격 + get_hogaunit_stock(주문가격) * 매도지정가호가번호)
        elif self.market_gubun == 4:
            return round(주문가격 + 0.01 * 매도지정가호가번호, 2)
        elif self.market_gubun == 5:
            return round(주문가격 + get_hogaunit_coin(주문가격) * 매도지정가호가번호, 8)
        elif self.market_gubun in (6, 7, 8):
            소숫점자리수 = self.dict_info[종목코드]['소숫점자리수']
            호가차이 = self.dict_info[종목코드]['호가단위'] * 매도지정가호가번호
            return round(주문가격 + 호가차이, 소숫점자리수) if 주문구분 == 'SELL_LONG' else round(주문가격 - 호가차이, 소숫점자리수)
        else:
            소숫점자리수 = self.dict_info[종목코드]['가격소숫점자리수']
            호가차이 = self.dict_info[종목코드]['호가단위'] * 매도지정가호가번호
            return round(주문가격 + 호가차이, 소숫점자리수) if 주문구분 == 'SELL_LONG' else round(주문가격 - 호가차이, 소숫점자리수)

    def _order_time_log(self, signal_time):
        gap = (now() - signal_time).total_seconds()
        self.windowQ.put((ui_num['타임로그'], f'시그널 주문 시간 알림 - 발생시간과 주문시간의 차이는 [{gap:.6f}]초입니다.'))

    def _get_order_code_list(self):
        if self.market_gubun < 6:
            return tuple(self.dict_order['매수']) + tuple(self.dict_order['매도'])
        else:
            return tuple(self.dict_order['BUY_LONG']) + tuple(self.dict_order['SELL_SHORT']) + \
                tuple(self.dict_order['SELL_LONG']) + tuple(self.dict_order['BUY_SHORT'])

    def _update_tuple(self, data):
        gubun, data = data
        if gubun == '잔고갱신':
            self._update_jango(data)
        elif gubun == '주문확인':
            code, c = data
            self.dict_curc[code] = c
            self._order_time_control(code)
        elif gubun == '저가대비고가등락율':
            self._set_leverage(data)
        if gubun == '관심진입':
            if self.market_gubun < 6:
                if data in self.dict_order['매도']:
                    self._cancel_order(data, '매도')
            else:
                if data in self.dict_order['SELL_LONG']:
                    self._cancel_order(data, 'SELL_LONG')
                if data in self.dict_order['BUY_SHORT']:
                    self._cancel_order(data, 'BUY_SHORT')
        elif gubun == '관심이탈':
            if self.market_gubun < 6:
                if data in self.dict_order['매수']:
                    self._cancel_order(data, '매수')
            else:
                if data in self.dict_order['BUY_LONG']:
                    self._cancel_order(data, 'BUY_LONG')
                if data in self.dict_order['SELL_SHORT']:
                    self._cancel_order(data, 'SELL_SHORT')
        elif gubun == '설정변경':
            self.dict_set = data
            self.jgcs_time = self.get_jgcs_time()
        elif gubun == '종목정보':
            if self.market_gubun < 5:
                self.dict_sgbn, self.dict_info = data
            else:
                self.dict_info = data
            self._update_dict_info()
            if self.market_gubun == 9:
                self._set_position()

    def _update_Jango(self, data):
        종목코드, 현재가 = data
        self.dict_curc[종목코드] = 현재가
        try:
            if 현재가 != self.dict_jg[종목코드]['현재가']:
                매입금액 = self.dict_jg[종목코드]['매입금액']
                보유수량 = self.dict_jg[종목코드]['보유수량']

                if self.market_gubun < 6 or self.market_gubun == 9:
                    보유금액 = 보유수량 * 현재가
                else:
                    매수가 = self.dict_jg[종목코드]['매수가']
                    보유금액 = 매입금액 + (현재가 - 매수가) * self.dict_info[종목코드]['틱가치'] * 보유수량

                if self.market_gubun < 6:
                    평가금액, 평가손익, 수익률 = self._get_profit(매입금액, 보유금액)
                else:
                    포지션 = self.dict_jg[종목코드]['포지션']
                    if 포지션 == 'LONG':
                        평가금액, 평가손익, 수익률 = self._get_profit_future_long(매입금액, 보유금액)
                    else:
                        평가금액, 평가손익, 수익률 = self._get_profit_future_short(매입금액, 보유금액)

                self.dict_jg[종목코드].update({
                    '현재가': 현재가,
                    '수익률': 수익률,
                    '평가손익': 평가손익,
                    '평가금액': 평가금액
                })
        except:
            pass

    def _get_profit(self, 매입금액, 보유금액):
        if self.market_gubun < 4:
            return get_profit_stock(매입금액, 보유금액)
        elif self.market_gubun == 4:
            return get_profit_stock_os(매입금액, 보유금액)
        else:
            return get_profit_coin(매입금액, 보유금액)

    def _get_profit_future_long(self, 매입금액, 보유금액):
        if self.market_gubun < 8:
            return get_profit_future_long(매입금액, 보유금액)
        elif self.market_gubun == 8:
            return get_profit_future_os_long(매입금액, 보유금액)
        else:
            return get_profit_coin_future_long(
                매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
            )

    def _get_profit_future_short(self, 매입금액, 보유금액):
        if self.market_gubun < 8:
            return get_profit_future_short(매입금액, 보유금액)
        elif self.market_gubun == 8:
            return get_profit_future_os_short(매입금액, 보유금액)
        else:
            return get_profit_coin_future_short(
                매입금액, 보유금액, '시장가' in self.dict_set['매수주문유형'], '시장가' in self.dict_set['매도주문유형']
            )

    def _update_dict_info(self):
        dummy_time = timedelta_sec(-3600)
        for code in self.dict_info.copy():
            self.dict_info[code].update({
                '시드부족시간': dummy_time,
                '최종거래시간': dummy_time,
                '손절거래시간': dummy_time
            })

    # noinspection PyUnresolvedReferences
    def _order_time_control(self, code_=None):
        cancel_list = []
        modify_list = []

        for gubun in self.dict_order:
            for code in self.dict_order[gubun]:
                if code_ is None or code == code_:
                    if self.market_gubun < 9:
                        주문취소시간, 정정횟수, 주문가격, 호가단위 = self.dict_order[gubun][code]
                    else:
                        주문취소시간, 정정횟수, 주문가격, 호가단위, _ = self.dict_order[gubun][code]

                    if self.market_gubun < 6:
                        매수매도구분 = gubun
                        범위이탈구분 = gubun == '매수'
                    else:
                        매수매도구분 = '매수' if gubun in ('BUY_LONG', 'SELL_SHORT') else '매도'
                        범위이탈구분 = 'BUY' in gubun

                    범위이탈 = False
                    호가차이 = 호가단위 * self.dict_set[f'{매수매도구분}정정호가차이']
                    현재가 = self.dict_curc.get(code)
                    if 현재가:
                        if 범위이탈구분:
                            범위이탈 = 현재가 >= 주문가격 + 호가차이
                        else:
                            범위이탈 = 현재가 <= 주문가격 - 호가차이

                    if self.dict_set[f'{매수매도구분}취소시간'] and now() > 주문취소시간:
                        cancel_list.append((code, gubun))

                    elif 정정횟수 < self.dict_set[f'{매수매도구분}정정횟수'] and 범위이탈:
                        정정호가 = self.dict_set[f'{매수매도구분}정정호가']
                        if 범위이탈구분:
                            if self.market_gubun < 4:
                                정정가격 = int(현재가 - 정정호가)
                            elif self.market_gubun == 4:
                                정정가격 = round(현재가 - 정정호가, 2)
                            elif self.market_gubun == 5:
                                정정가격 = round(현재가 - 정정호가, 8)
                            elif self.market_gubun in (6, 7, 8):
                                정정가격 = round(현재가 - 정정호가, self.dict_info[code]['소숫점자리수'])
                            else:
                                정정가격 = round(현재가 - 정정호가, self.dict_info[code]['가격소숫점자리수'])
                        else:
                            if self.market_gubun < 4:
                                정정가격 = int(현재가 + 정정호가)
                            elif self.market_gubun == 4:
                                정정가격 = round(현재가 + 정정호가, 2)
                            elif self.market_gubun == 5:
                                정정가격 = round(현재가 + 정정호가, 8)
                            elif self.market_gubun in (6, 7, 8):
                                정정가격 = round(현재가 + 정정호가, self.dict_info[code]['소숫점자리수'])
                            else:
                                정정가격 = round(현재가 + 정정호가, self.dict_info[code]['가격소숫점자리수'])
                        modify_list.append((code, gubun, 정정가격))

        if cancel_list:
            for code, gubun in cancel_list:
                self._cancel_order(code, gubun)
        if modify_list:
            for code, gubun, 정정가격 in modify_list:
                self._modify_order(code, gubun, 정정가격)

    def _cancel_order(self, 종목코드, 주문구분):
        종목명 = self.dict_info[종목코드]['종목명']
        last_value = self._get_chejan_last_value(종목명, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                원주문번호, 원주문가격 = last_value['주문번호'], last_value['주문가격']
                if self.market_gubun < 6:
                    self._create_order(
                        f'{주문구분}취소', 종목코드, 종목명, 원주문가격, 미체결수량, 원주문번호, now(), False, 0, None
                    )
                else:
                    self._create_order(
                        f'{주문구분}_CANCEL', 종목코드, 종목명, 원주문가격, 미체결수량, 원주문번호, now(), False, 0, None
                    )

    def _modify_order(self, 종목코드, 주문구분, 정정가격):
        종목명 = self.dict_info[종목코드]['종목명']
        last_value = self._get_chejan_last_value(종목명, 주문구분)
        if last_value:
            미체결수량 = last_value['미체결수량']
            if 미체결수량 > 0:
                정정횟수 = self.dict_order[주문구분][종목코드][1] + 1
                원주문번호, 원주문가격 = last_value['주문번호'], last_value['주문가격']
                if self.market_gubun < 5:
                    self._create_order(
                        f'{주문구분}정정', 종목코드, 종목명, 정정가격, 미체결수량, 원주문번호, now(), False, 정정횟수, None
                    )
                elif self.market_gubun == 5:
                    self._create_order(
                        f'{주문구분}취소', 종목코드, 종목명, 원주문가격, 미체결수량, 원주문번호, now(), False, 0, None
                    )
                    self._create_order(
                        주문구분, 종목코드, 종목명, 정정가격, 미체결수량, '', now(), False, 정정횟수, None
                    )
                elif self.market_gubun < 9:
                    self._create_order(
                        f'{주문구분}_MODIFY', 종목코드, 종목명, 정정가격, 미체결수량, 원주문번호, now(), False, 정정횟수, None
                    )
                else:
                    self._create_order(
                        f'{주문구분}_CANCEL', 종목코드, 종목코드, 원주문가격, 미체결수량, 원주문번호, now(), False, 0, None
                    )
                    self._create_order(
                        주문구분, 종목코드, 종목코드, 정정가격, 미체결수량, '', now(), False, 정정횟수, None
                    )

    def _get_chejan_last_value(self, code, gubun):
        if self.market_gubun < 6:
            return [v for v in self.dict_cj.values() if v['종목명'] == code and
                    (v['주문구분코드'] == gubun or v['주문구분코드'] == f'{gubun} 접수')][-1]
        else:
            return [v for v in self.dict_cj.values() if v['종목명'] == code and
                    (v['주문구분코드'] == gubun or v['주문구분코드'] == f'{gubun}_REG')][-1]

    def _update_string(self, data):
        if data == '체결목록':
            df_cj = pd.DataFrame.from_dict(self.dict_cj, orient='index')
            self.teleQ.put(df_cj if len(df_cj) > 0 else f"현재는 {self.market_info['마켓이름']} 체결목록이 없습니다.")
        elif data == '거래목록':
            df_td = pd.DataFrame.from_dict(self.dict_td, orient='index')
            self.teleQ.put(df_td if len(df_td) > 0 else f"현재는 {self.market_info['마켓이름']} 거래목록이 없습니다.")
        elif data == '잔고평가':
            df_jg = pd.DataFrame.from_dict(self.dict_jg, orient='index')
            self.teleQ.put(df_jg if len(df_jg) > 0 else f"현재는 {self.market_info['마켓이름']} 잔고목록이 없습니다.")
        elif data == '잔고청산':
            self._jango_cheongsan('수동')
        elif data == '프로세스종료':
            self._sys_exit()

    def _jango_cheongsan(self, gubun):
        for 주문구분 in self.dict_order:
            for 종목코드 in self.dict_order[주문구분]:
                self._cancel_order(종목코드, 주문구분)

        if self.dict_jg:
            if gubun == '수동':
                self.teleQ.put(f"{self.market_info['마켓이름']} 잔고청산 주문을 전송합니다.")
            for 종목코드 in self.dict_jg.copy():
                종목명 = self.dict_jg[종목코드]['종목명']
                현재가 = self.dict_jg[종목코드]['현재가']
                보유수량 = self.dict_jg[종목코드]['보유수량']
                if self.market_gubun < 6:
                    주문구분 = '매도'
                else:
                    포지션 = self.dict_jg[종목코드]['포지션']
                    주문구분 = 'SELL_LONG' if 포지션 == 'LONG' else 'BUY_SHORT'
                if self.dict_set['모의투자']:
                    주문시간 = self._get_str_ymdhms()
                    self._update_chejan_data(주문구분, 종목코드, 보유수량, 보유수량, 0, 현재가, 현재가, 주문시간, '')
                else:
                    self._check_order((주문구분, 종목코드, 종목명, 현재가, 보유수량, now(), True))
            if self.dict_set['알림소리']:
                self.soundQ.put(f"{self.market_info['마켓이름']} 잔고청산 주문을 전송하였습니다.")
            self.windowQ.put((ui_num['기본로그'], f"시스템 명령 실행 알림 - {self.market_info['마켓이름']} 잔고청산 주문 완료"))
        elif gubun == '수동':
            self.teleQ.put(f"현재는 {self.market_info['마켓이름']} 보유종목이 없습니다.")
        self.dict_bool['잔고청산'] = True

    def _sys_exit(self):
        self._websocket_kill()
        self.windowQ.put((ui_num['기본로그'], f"시스템 명령 실행 알림 - {self.market_info['마켓이름']} 트레이더 종료"))

    def _websocket_kill(self):
        if self.ws_thread:
            self.ws_thread.stop()
            self.ws_thread.terminate()

    def _get_index(self):
        index = str_ymdhmsf(now_cme())
        if index in self.dict_cj:
            while index in self.dict_cj:
                index = str(int(index) + 1)
        return index

    def _update_tradelist(self, index, 종목명, 매입금액, 평가금액, 체결수량, 수익률, 수익금, 주문시간, 포지션=None):
        """['종목명', '포지션', '매수금액', '매도금액', '주문수량', '수익률', '수익금', '체결시간']"""
        if 포지션 is None:
            """['종목명', '매수금액', '매도금액', '주문수량', '수익률', '수익금', '체결시간']"""
            self.dict_td[index] = {
                '종목명': 종목명,
                '포지션': 포지션,
                '매수금액': 매입금액,
                '매도금액': 평가금액,
                '주문수량': 체결수량,
                '수익률': 수익률,
                '수익금': 수익금,
                '체결시간': 주문시간
            }
        else:
            """['종목명', '포지션', '매수금액', '매도금액', '주문수량', '수익률', '수익금', '체결시간']"""
            self.dict_td[index] = {
                '종목명': 종목명,
                '포지션': 포지션,
                '매수금액': 매입금액,
                '매도금액': 평가금액,
                '주문수량': 체결수량,
                '수익률': 수익률,
                '수익금': 수익금,
                '체결시간': 주문시간
            }

        df_td = pd.DataFrame.from_dict(self.dict_td, orient='index')
        self.windowQ.put((ui_num['거래목록'], df_td[::-1]))

        if 포지션 is None:
            data = [[종목명, 포지션, 매입금액, 평가금액, 체결수량, 수익률, 수익금, 주문시간]]
            columns = columns_tdf
        else:
            data = [[종목명, 매입금액, 평가금액, 체결수량, 수익률, 수익금, 주문시간]]
            columns = columns_td
        df = pd.DataFrame(data, columns=columns, index=[index])
        self.queryQ.put(('거래디비', df, self.market_info['거래디비'], 'append'))

        self._update_totaltradelist()

    def _update_totaltradelist(self, first=False):
        td_values = self.dict_td.values()
        거래횟수 = len(set([(v['종목명'], v['체결시간']) for v in td_values]))
        총매수금액 = sum([v['매수금액'] for v in td_values])
        총매도금액 = sum([v['매도금액'] for v in td_values])
        총수익금액 = sum([v['수익금'] for v in td_values if v['수익금'] >= 0])
        총손실금액 = sum([v['수익금'] for v in td_values if v['수익금'] < 0])
        수익금합계 = sum([v['수익금'] for v in td_values])
        수익률 = round(수익금합계 / self.dict_intg['추정예탁자산'] * 100, 2)

        # ['거래횟수', '총매수금액', '총매도금액', '총수익금액', '총손실금액', '수익률', '수익금합계']
        self.dict_tt[self.str_today] = {
            '거래횟수': 거래횟수,
            '총매수금액': 총매수금액,
            '총매도금액': 총매도금액,
            '총수익금액': 총수익금액,
            '총손실금액': 총손실금액,
            '수익률': 수익률,
            '수익금합계': 수익금합계
        }
        df_tt = pd.DataFrame.from_dict(self.dict_tt, orient='index')
        delete_query = f"DELETE FROM {self.market_info['손익디비']} WHERE `index` = '{self.str_today}'"
        self.queryQ.put(('거래디비', delete_query))
        self.queryQ.put(('거래디비', df_tt, self.market_info['손익디비'], 'append'))
        self.windowQ.put((ui_num['실현손익'], df_tt))

        if not first:
            self.teleQ.put(df_tt)

        if self.dict_set['스톰라이브']:
            수익률 = round(수익금합계 / 총매수금액 * 100, 2)
            data_list = [거래횟수, 총매수금액, 총매도금액, 총수익금액, 총손실금액, 수익률, 수익금합계]
            self.liveQ.put(('', data_list))

    def _update_chegeollist(self, index, 종목코드, 종목명, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 체결시간, 주문가격, 주문번호):
        # ['종목명', '주문구분코드', '주문수량', '체결수량', '미체결수량', '체결가', '체결시간', '주문가격', '주문번호']
        self.dict_info[종목코드]['최종거래시간'] = timedelta_sec(self.dict_set['매수금지간격초'])
        self.dict_cj[index] = {
            '종목명': 종목명,
            '주문구분코드': 주문구분,
            '주문수량': 주문수량,
            '체결수량': 체결수량,
            '미체결수량': 미체결수량,
            '체결가': 체결가격,
            '체결시간': 체결시간,
            '주문가격': 주문가격,
            '주문번호': 주문번호
        }
        self.dict_cj = dict(sorted(self.dict_cj.items(), key=lambda x: x[0]))
        df_cj = pd.DataFrame.from_dict(self.dict_cj, orient='index')
        self.windowQ.put((ui_num['체결목록'], df_cj[::-1]))
        df = pd.DataFrame(
            [[종목코드, 주문구분, 주문수량, 체결수량, 미체결수량, 체결가격, 체결시간, 주문가격, 주문번호]],
            columns=columns_cj,
            index=[index]
        )
        self.queryQ.put(('거래디비', df, self.market_info['체결디비'], 'append'))

    def _update_totaljango(self):
        # ['추정예탁자산', '추정예수금', '보유종목수', '수익률', '총평가손익', '총매입금액', '총평가금액']
        if self.dict_jg:
            jg_values = self.dict_jg.values()
            총평가손익 = sum([v['평가손익'] for v in jg_values])
            총매입금액 = sum([v['매입금액'] for v in jg_values])
            총평가금액 = sum([v['평가금액'] for v in jg_values])
            총수익률 = round(총평가손익 / 총매입금액 * 100, 2)
            잔고수량 = len(self.dict_jg)
            추정예탁자산 = self.dict_intg['예수금'] + 총평가금액
        else:
            총평가손익, 총매입금액, 총평가금액, 총수익률, 잔고수량 = 0, 0, 0, 0., 0
            추정예탁자산 = self.dict_intg['예수금']

        self.dict_tj[self.str_today] = {
            '추정예탁자산': 추정예탁자산,
            '추정예수금': self.dict_intg['예수금'],
            '보유종목수': 잔고수량,
            '수익률': 총수익률,
            '총평가손익': 총평가손익,
            '총매입금액': 총매입금액,
            '총평가금액': 총평가금액
        }

        거래수익금합계 = sum([v['수익금'] for v in self.dict_td.values()])
        당일평가손익 = 총평가손익 + 거래수익금합계
        if self.dict_set['손실중지']:
            기준손실금 = self.dict_intg['추정예탁자산'] * self.dict_set['손실중지수익률'] / 100
            if 기준손실금 < -당일평가손익:
                self._strategy_stop()
        if self.dict_set['수익중지']:
            기준수익금 = self.dict_intg['추정예탁자산'] * self.dict_set['수익중지수익률'] / 100
            if 기준수익금 < 당일평가손익:
                self._strategy_stop()

        if self.dict_set['투자금고정']:
            종목당투자금 = int(self.dict_set['투자금'] * (1_000_000 if self.market_gubun in (1, 2, 3, 5) else 1))
        else:
            종목당투자금 = int(self.dict_intg['추정예탁자산'] * 0.98 / self.dict_set['최대매수종목수'])

        if self.dict_intg['종목당투자금'] != 종목당투자금:
            self.dict_intg['종목당투자금'] = 종목당투자금
            if self.market_gubun < 5:
                for q in self.stgQs:
                    q.put(('종목당투자금', self.dict_intg['종목당투자금']))
            else:
                self.stgQ.put(('종목당투자금', self.dict_intg['종목당투자금']))

        if self.dict_jg:
            df_jg = pd.DataFrame.from_dict(self.dict_jg, orient='index')
        else:
            df_jg = pd.DataFrame(columns=columns_jg)
        df_tj = pd.DataFrame.from_dict(self.dict_tj, orient='index')
        self.windowQ.put((ui_num['잔고목록'], df_jg))
        self.windowQ.put((ui_num['잔고평가'], df_tj))

    def _strategy_stop(self):
        if self.market_gubun < 5:
            for q in self.stgQs:
                q.put('매수전략중지')
        else:
            self.stgQ.put('매수전략중지')
        self._jango_cheongsan('수동')

    def _set_position(self):
        pass

    def _set_leverage(self, data):
        pass

    def _update_jango(self, data):
        pass

    def _send_order(self, data):
        pass

    def _convert_order_data(self, data):
        pass

    def _update_chejan_data(self, 주문구분, 종목코드, 주문수량, 체결수량, 미체결수량, 체결가격, 주문가격, 주문시간, 주문번호):
        pass
