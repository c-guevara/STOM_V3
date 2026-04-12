
import sqlite3
import pandas as pd
from copy import deepcopy
from traceback import format_exc
from utility.setting_base import indicator
from trade.risk_analyzer import RiskAnalyzer
from trade.formula_manager import get_formula_data
from trade.strategy_globals_func import StrategyGlobalsFunc
from utility.static import get_ema_list, now, set_builtin_print
from trade.microstructure_analyzer import MicrostructureAnalyzer
from utility.setting_base import DB_STRATEGY, ui_num, dict_order_ratio


class BaseStrategy(StrategyGlobalsFunc):
    def __init__(self, gubun, qlist, dict_set, market_info):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, receivQ, traderQ, stgQs, liveQ
           0        1       2      3       4      5      6      7       8        9       10     11
        """
        super().__init__()
        self.gubun           = gubun
        self.windowQ         = qlist[0]
        self.teleQ           = qlist[3]
        self.traderQ         = qlist[9]
        self.stgQs           = qlist[10]
        self.stgQ            = qlist[10][self.gubun]
        self.dict_set        = dict_set
        self.indicator       = indicator
        self.market_gubun    = market_info[0]
        self.market_info     = market_info[1]

        self.buystrategy     = None
        self.sellstrategy    = None
        self.chart_code      = None
        self.arry_code       = None
        self.info_for_buy    = None
        self.info_for_sell   = None

        self.dict_data: dict[str, list] = {}
        self.dict_gj: dict[str, dict[str, int | float]] = {}
        self.dict_jg: dict[str, dict[str, int | float]] = {}
        self.dict_profit: dict[str, list] = {}

        self.dict_info       = {}
        self.dict_signal     = {}
        self.dict_buy_num    = {}
        self.dict_signal_num = {}
        self.indi_settings   = []

        self.jgrv_count      = 0
        self.int_tujagm      = 0
        self.비중조절기준       = 0

        self.avg_list        = [self.dict_set['평균값계산틱수']]
        self.rolling_window  = self.dict_set['평균값계산틱수']

        self.is_tick         = self.dict_set['타임프레임']
        self.buy_hj_limit    = self.dict_set['매수시장가잔량범위']
        self.sell_hj_limit   = self.dict_set['매도시장가잔량범위']
        self.set_weight      = self.dict_set['비중조절']
        self.sma_list        = get_ema_list(self.is_tick)

        self.ma_round_unit   = self.market_info['반올림단위']
        self.angle_pct_cf    = self.market_info['각도계수'][self.is_tick][0]
        self.angle_dtm_cf    = self.market_info['각도계수'][self.is_tick][1]
        factor_list          = self.market_info['팩터목록'][self.is_tick]
        self.dict_findex     = {factor: i for i, factor in enumerate(factor_list)}
        self.data_cnt        = self.market_info['팩터개수'][self.is_tick]

        self.base_cnt        = self.dict_findex['관심종목'] + 1
        self.area_cnt        = self.dict_findex['당일거래대금각도'] + 1

        if self.is_tick:
            self.dict_findex['초당매도수금액'] = self.dict_findex['초당매수금액']
            self.dict_findex['누적초당매도수수량'] = self.dict_findex['누적초당매수수량']
        else:
            self.dict_findex['분당매도수금액'] = self.dict_findex['분당매수금액']
            self.dict_findex['누적분당매도수수량'] = self.dict_findex['누적분당매수수량']

        self.dict_findex['당일매도수금액'] = self.dict_findex['당일매수금액']
        self.dict_findex['최고매도수금액'] = self.dict_findex['최고매수금액']
        self.dict_findex['최고매도수가격'] = self.dict_findex['최고매수가격']
        self.dict_findex['호가총잔량'] = self.dict_findex['매수총잔량']
        self.dict_findex['매도수호가잔량1'] = self.dict_findex['매수잔량1']

        self.ms_analyzer = MicrostructureAnalyzer(self.market_info['마켓구분'], factor_list)
        self.rk_analyzer = RiskAnalyzer(self.market_info['마켓구분'], factor_list)

        set_builtin_print(self.windowQ)

    def _set_formula_data(self):
        self.fm_list, dict_fm, self.fm_tcnt = get_formula_data(False, self.data_cnt)
        self.windowQ.put((ui_num['사용자수식'], deepcopy(self.fm_list), dict_fm, self.fm_tcnt))
        if self.fm_list:
            for fm in self.fm_list:
                fm[8] = compile(fm[-2], '<string>', 'exec')

    def _update_stringategy(self):
        table_name_stg_buy       = f"{self.market_info['전략구분']}_buy"
        table_name_stg_sell      = f"{self.market_info['전략구분']}_sell"
        table_name_stg_optibuy   = f"{self.market_info['전략구분']}_optibuy"
        table_name_stg_optisell  = f"{self.market_info['전략구분']}_optisell"
        table_name_stg_passticks = f"{self.market_info['전략구분']}_passticks"
        con  = sqlite3.connect(DB_STRATEGY)
        dfb  = pd.read_sql(f'SELECT * FROM {table_name_stg_buy}', con).set_index('index')
        dfs  = pd.read_sql(f'SELECT * FROM {table_name_stg_sell}', con).set_index('index')
        dfob = pd.read_sql(f'SELECT * FROM {table_name_stg_optibuy}', con).set_index('index')
        dfos = pd.read_sql(f'SELECT * FROM {table_name_stg_optisell}', con).set_index('index')
        dfpt = pd.read_sql(f'SELECT * FROM {table_name_stg_passticks}', con).set_index('index')
        con.close()

        self._set_strategy(dfs, dfos, dfb, dfob)
        if len(dfpt) > 0:
            self._set_passticks(dfpt)

        self.set_globals_func()

    def _set_strategy(self, dfs, dfos, dfb, dfob):
        if self.dict_set['매도전략'] in dfs.index:
            self.sellstrategy = compile(dfs['전략코드'][self.dict_set['매도전략']], '<string>', 'exec')
        elif self.dict_set['매도전략'] in dfos.index:
            self.sellstrategy = compile(dfos['전략코드'][self.dict_set['매도전략']], '<string>', 'exec')

        buytxt = ''
        if self.dict_set['매수전략'] in dfb.index:
            buytxt = dfb['전략코드'][self.dict_set['매수전략']]
        elif self.dict_set['매수전략'] in dfob.index:
            buytxt = dfob['전략코드'][self.dict_set['매수전략']]
            vars_text = dfob['변수값'][self.dict_set['매수전략']]
            if vars_text != '':
                vars_list = [float(i) if '.' in i else int(i) for i in vars_text.split(';')]
                self.vars = {i: var for i, var in enumerate(vars_list)}

        self._set_buy_strategy(buytxt)

    def _set_buy_strategy(self, buytxt):
        self.buystrategy, indistg = self.get_buy_indi_stg(buytxt)
        if indistg is not None:
            try:
                exec(indistg)
            except:
                self.windowQ.put((ui_num['시스템로그'], f'{format_exc()}오류 알림 - indistg'))
        self.indi_settings = list(self.indicator.values())

    def get_buy_indi_stg(self, buytxt):
        lines   = [line for line in buytxt.split('\n') if line and line[0] != '#']
        buystg  = '\n'.join(line for line in lines if 'self.indicator' not in line)
        indistg = '\n'.join(line for line in lines if 'self.indicator' in line)
        if buystg:
            try:
                buystg = compile(buystg, '<string>', 'exec')
            except:
                buystg = None
        else:
            buystg = None
        if indistg:
            try:
                indistg = compile(indistg, '<string>', 'exec')
            except:
                indistg = None
        else:
            indistg = None
        return buystg, indistg

    def _set_passticks(self, dfpt):
        def compile_condition(x):
            return compile(f'if {x}:\n    self.dict_cond_indexn[종목코드][k] = self.indexn', '<string>', 'exec')

        name_list = list(dfpt.index)
        stg_list  = dfpt['전략코드'].to_list()
        stg_list  = [compile_condition(x) for x in stg_list]
        self.dict_condition = dict(zip(name_list, stg_list))

    def _main_loop(self):
        self.windowQ.put((ui_num['기본로그'], f"시스템 명령 실행 알림 - {self.market_info['마켓이름']} 전략 연산 시작"))
        while True:
            try:
                data = self.stgQ.get()
                if data.__class__ == list:
                    self._strategy(data)
                elif data.__class__ == tuple:
                    self._update_tuple(data)
                elif data.__class__ == str:
                    self._update_string(data)
            except:
                from traceback import format_exc
                self.windowQ.put((ui_num['시스템로그'], format_exc()))

    def _update_tuple(self, data):
        gubun, data = data
        if gubun == '잔고목록':
            self.dict_jg = data
            self.jgrv_count += 1
            if self.jgrv_count == 2:
                self.jgrv_count = 0
                self._put_gsjm_and_delete_hilo()
        elif gubun == '관심목록':
            self.dict_gj = {k: v for k, v in self.dict_gj.items() if k in data}
        elif gubun in ('매수완료', '매수취소'):
            if data in self.dict_signal['매수']:
                self.dict_signal['매수'].remove(data)
            if gubun == '매수완료':
                self.dict_buy_num[data] = self.dict_signal_num.get(data, len(self.dict_data[data]) - 1)
        elif gubun in ('매도완료', '매도취소'):
            if data in self.dict_signal['매도']:
                self.dict_signal['매도'].remove(data)
        elif gubun == '매수주문':
            if data not in self.dict_signal['매수']:
                self.dict_signal['매수'].append(data)
        elif gubun == '매도주문':
            if data not in self.dict_signal['매도']:
                self.dict_signal['매도'].append(data)
        elif '_COMPLETE' in gubun:
            gubun = gubun.replace('_COMPLETE', '')
            if data in self.dict_signal[gubun]:
                self.dict_signal[gubun].remove(data)
            if gubun in ('BUY_LONG', 'SELL_SHORT'):
                self.dict_buy_num[data] = self.dict_signal_num.get(data, len(self.dict_data[data]) - 1)
        elif '_CANCEL' in gubun:
            gubun = gubun.replace('_CANCEL', '')
            if data in self.dict_signal[gubun]:
                self.dict_signal[gubun].remove(data)
        elif '_MANUAL' in gubun:
            gubun = gubun.replace('_MANUAL', '')
            if data not in self.dict_signal[gubun]:
                self.dict_signal[gubun].append(data)
        elif gubun == '매수전략':
            self._set_buy_strategy(data)
        elif gubun == '매도전략':
            self.sellstrategy = compile(data, '<string>', 'exec')
        elif gubun == '종목당투자금':
            self.int_tujagm = data
        elif gubun == '차트종목코드':
            self.chart_code = data
        elif gubun == '설정변경':
            self.dict_set = data
            self._update_stringategy()
        elif gubun == '종목정보':
            self.dict_info = data
        elif gubun == '데이터저장':
            self._save_data(data)

    def _update_string(self, data):
        if data == '매수전략중지':
            self.buystrategy = None
            self.teleQ.put('매수전략 중지 완료')
        elif data == '매도전략중지':
            self.sellstrategy = None
            self.teleQ.put('매도전략 중지 완료')
        elif data == '프로세스종료':
            self.windowQ.put((ui_num['기본로그'], f"시스템 명령 실행 알림 - {self.market_info['마켓이름']} 전략연산 종료"))

    def _get_parameter_area(self, rw):
        if self.is_tick:
            return [
                self._이동평균(self.sma_list[0], calc=True), self._이동평균(self.sma_list[1], calc=True),
                self._이동평균(self.sma_list[2], calc=True), self._이동평균(self.sma_list[3], calc=True),
                self._이동평균(self.sma_list[4], calc=True), self._최고현재가(rw, calc=True), self._최저현재가(rw, calc=True),
                self._체결강도평균(rw, calc=True), self._최고체결강도(rw, calc=True), self._최저체결강도(rw, calc=True),
                self._최고초당매수수량(rw, calc=True), self._최고초당매도수량(rw, calc=True), self._누적초당매수수량(rw, calc=True),
                self._누적초당매도수량(rw, calc=True), self._초당거래대금평균(rw, calc=True), self._등락율각도(rw, calc=True),
                self._당일거래대금각도(rw, calc=True)
            ]
        else:
            return [
                self._이동평균(self.sma_list[0], calc=True), self._이동평균(self.sma_list[1], calc=True),
                self._이동평균(self.sma_list[2], calc=True), self._이동평균(self.sma_list[3], calc=True),
                self._이동평균(self.sma_list[4], calc=True), self._최고현재가(rw, calc=True), self._최저현재가(rw, calc=True),
                self._최고분봉고가(rw, calc=True), self._최저분봉저가(rw, calc=True), self._체결강도평균(rw, calc=True),
                self._최고체결강도(rw, calc=True), self._최저체결강도(rw, calc=True), self._최고분당매수수량(rw, calc=True),
                self._최고분당매도수량(rw, calc=True), self._누적분당매수수량(rw, calc=True), self._누적분당매도수량(rw, calc=True),
                self._분당거래대금평균(rw, calc=True), self._등락율각도(rw, calc=True), self._당일거래대금각도(rw, calc=True)
            ]

    def Buy(self, buy_long=False):
        취소시그널, 분할매수횟수, 매수가, 현재가, 저가대비고가등락율, 매도호가1, 매수호가1 = self.info_for_buy
        if 취소시그널:
            주문수량 = 0
        else:
            주문수량 = self._set_buy_count(분할매수횟수, 매수가, 현재가, 저가대비고가등락율)

        if self.market_gubun < 6:
            signal_gubun = '매수'
        else:
            signal_gubun = 'BUY_LONG' if buy_long else 'SELL_SHORT'

        if '지정가' in self.dict_set['매수주문유형']:
            기준가격 = 현재가
            if self.dict_set['매수지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1 if self.market_gubun < 6 or buy_long else 매수호가1
            if self.dict_set['매수지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1 if self.market_gubun < 6 or buy_long else 매도호가1
            self.dict_signal[signal_gubun].append(self.code)
            self.dict_signal_num[self.code] = self.indexn
            self.traderQ.put((signal_gubun, self.code, self.name, 기준가격, 주문수량, now(), False))
        else:
            if self.market_gubun < 6 or buy_long:
                호가배열 = self.shogainfo[:self.buy_hj_limit]
                잔량배열 = self.shreminfo[:self.buy_hj_limit]
            else:
                호가배열 = self.bhogainfo[:self.buy_hj_limit]
                잔량배열 = self.bhreminfo[:self.buy_hj_limit]

            거래금액, 체결완료 = self._calc_fill_amount(주문수량, 호가배열, 잔량배열)
            if 체결완료:
                예상체결가 = self._get_order_price(거래금액, 주문수량)
                self.dict_signal[signal_gubun].append(self.code)
                self.dict_signal_num[self.code] = self.indexn
                self.traderQ.put((signal_gubun, self.code, self.name, 예상체결가, 주문수량, now(), False))

    def _get_buy_count(self, 분할매수횟수, 매수가, 현재가, 저가대비고가등락율):
        if self.dict_set['비중조절'][0] == 0:
            betting = self.int_tujagm
        else:
            if self.dict_set['비중조절'][0] == 1:
                비중조절기준 = 저가대비고가등락율
            elif self.dict_set['비중조절'][0] == 2:
                비중조절기준 = self._거래대금평균대비비율(30)
            elif self.dict_set['비중조절'][0] == 3:
                비중조절기준 = self._등락율각도(30)
            elif self.dict_set['비중조절'][0] == 4:
                비중조절기준 = self._당일거래대금각도(30)
            else:
                비중조절기준 = self.비중조절기준

            if 비중조절기준 < self.dict_set['비중조절'][1]:
                betting = self.int_tujagm * self.dict_set['비중조절'][5]
            elif 비중조절기준 < self.dict_set['비중조절'][2]:
                betting = self.int_tujagm * self.dict_set['비중조절'][6]
            elif 비중조절기준 < self.dict_set['비중조절'][3]:
                betting = self.int_tujagm * self.dict_set['비중조절'][7]
            elif 비중조절기준 < self.dict_set['비중조절'][4]:
                betting = self.int_tujagm * self.dict_set['비중조절'][8]
            else:
                betting = self.int_tujagm * self.dict_set['비중조절'][9]

        oc_ratio = dict_order_ratio[self.dict_set['매수분할방법']][self.dict_set['매수분할횟수']][분할매수횟수]
        매수수량 = self._set_buy_count(betting, 현재가, 매수가, oc_ratio)
        return 매수수량

    def Sell(self, sell_long=False):
        취소시그널, 전량매도, 강제청산, 보유수량, 분할매도횟수, 매수가, 현재가, 저가대비고가등락율, 매도호가1, 매수호가1 = self.info_for_sell
        if 취소시그널:
            주문수량 = 0
        elif 전량매도:
            주문수량 = 보유수량
        else:
            주문수량 = self._get_sell_count(분할매도횟수, 보유수량)

        if self.market_gubun < 6:
            signal_gubun = '매도'
        else:
            signal_gubun = 'SELL_LONG' if sell_long else 'BUY_SHORT'

        if '지정가' in self.dict_set['매도주문유형'] and not 강제청산:
            기준가격 = 현재가
            if self.dict_set['매도지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1 if self.market_gubun < 6 or sell_long else 매수호가1
            if self.dict_set['매도지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1 if self.market_gubun < 6 or sell_long else 매도호가1
            self.dict_signal[signal_gubun].append(self.code)
            self.traderQ.put((signal_gubun, self.code, self.name, 기준가격, 주문수량, now(), False))
        else:
            if self.market_gubun < 6 or sell_long:
                호가배열 = self.bhogainfo[:self.sell_hj_limit]
                잔량배열 = self.bhreminfo[:self.sell_hj_limit]
            else:
                호가배열 = self.shogainfo[:self.sell_hj_limit]
                잔량배열 = self.shreminfo[:self.sell_hj_limit]

            거래금액, 체결완료 = self._calc_fill_amount(주문수량, 호가배열, 잔량배열)
            if 체결완료:
                예상체결가 = self._get_order_price(거래금액, 주문수량)
                self.dict_signal[signal_gubun].append(self.code)
                self.traderQ.put((signal_gubun, self.code, self.name, 예상체결가, 주문수량, now(), True if 강제청산 else False))

    def _get_sell_count(self, 분할매도횟수, 보유수량):
        if self.dict_set['매도분할횟수'] == 1:
            return 보유수량
        else:
            dict_ratio = dict_order_ratio[self.dict_set['매도분할방법']][self.dict_set['매도분할횟수']]
            oc_ratio = dict_ratio[분할매도횟수]
            보유비율 = sum(비율 for 횟수, 비율 in dict_ratio.items() if 횟수 >= 분할매도횟수)
            매도수량 = self._set_sell_count(보유수량, 보유비율, oc_ratio)
            if 매도수량 > 보유수량 or 분할매도횟수 + 1 == self.dict_set['매도분할횟수']:
                매도수량 = 보유수량
            return 매도수량

    def _put_gsjm_and_delete_hilo(self):
        if self.dict_gj:
            self.dict_gj = dict(sorted(self.dict_gj.items(), key=lambda x: x[1]['dm'], reverse=True))
            df_gj = pd.DataFrame.from_dict(self.dict_gj, orient='index')
            if self.market_gubun < 5:
                self.windowQ.put((ui_num['관심종목'], self.gubun, df_gj))
            else:
                self.windowQ.put((ui_num['관심종목'], df_gj))
        if self.dict_profit:
            self.dict_profit = {k: v for k, v in self.dict_profit.items() if k in self.dict_jg}

    def _save_data(self, codes):
        for code in self.dict_data.copy():
            if code not in codes:
                del self.dict_data[code]

        last = len(self.dict_data)
        columns_ = self.market_info['팩터목록'][self.is_tick][:self.base_cnt]
        con = sqlite3.connect(self.market_info['당일디비'][self.is_tick])
        if last > 0:
            start = now()
            cllen = len(columns_)
            for i, code in enumerate(self.dict_data):
                df = pd.DataFrame(self.dict_data[code][:, :cllen], columns=columns_)
                df['index'] = df['index'].astype('int64')
                df.to_sql(code, con, index=False, if_exists='append', chunksize=2000)
                log_text = f'시스템 명령 실행 알림 - 전략연산 프로세스 데이터 저장 중 ... [{self.gubun + 1}]{i + 1}/{last}'
                self.windowQ.put((ui_num['기본로그'], log_text))
            save_time = (now() - start).total_seconds()
            self.windowQ.put((ui_num['기본로그'], f'시스템 명령 실행 알림 - 데이터 저장 쓰기소요시간은 [{save_time:.6f}]초입니다.'))
        con.close()

        if self.market_gubun < 5:
            if self.gubun != 7:
                self.stgQs[self.gubun + 1].put(('데이터저장', codes))
            else:
                self.stgQs[self.gubun].put('프로세스종료')
        else:
            self.stgQ.put('프로세스종료')

    def _update_high_low(self, 종목코드, 현재가또는분봉고가, 분봉저가=None):
        if 분봉저가 is None:
            high_low = self.high_low.get(종목코드)
            if high_low:
                if 현재가또는분봉고가 >= high_low[0]:
                    high_low[0] = 현재가또는분봉고가
                    high_low[1] = self.indexn
                if 현재가또는분봉고가 <= high_low[2]:
                    high_low[2] = 현재가또는분봉고가
                    high_low[3] = self.indexn
            else:
                self.high_low[종목코드] = [현재가또는분봉고가, self.indexn, 현재가또는분봉고가, self.indexn]
        else:
            high_low = self.high_low.get(종목코드)
            if high_low:
                if 현재가또는분봉고가 >= high_low[0]:
                    high_low[0] = 현재가또는분봉고가
                    high_low[1] = self.indexn
                if 분봉저가 <= high_low[2]:
                    high_low[2] = 분봉저가
                    high_low[3] = self.indexn
            else:
                self.high_low[종목코드] = [현재가또는분봉고가, self.indexn, 분봉저가, self.indexn]

    def _strategy(self, data):
        pass

    def _get_order_price(self, 거래금액, 주문수량):
        return 0

    def _set_buy_count(self, betting, 현재가, 매수가, oc_ratio):
        return 0

    def _set_sell_count(self, 보유수량, 보유비율, oc_ratio):
        return 0
