
import time
import sqlite3
import pandas as pd
from copy import deepcopy
from traceback import format_exc
from trade.risk_analyzer import RiskAnalyzer
from trade.formula_manager import get_formula_data
from trade.base_globals_func import BaseGlobalsFunc
from utility.static import get_ema_list, now, get_profile_text
from utility.setting_base import DB_STRATEGY, ui_num, dict_order_ratio
from trade.microstructure_analyzer import MicrostructureAnalyzer
from utility.setting_base import indicator, DICT_MARKET_GUBUN, DICT_MARKET_INFO


class BaseStrategy(BaseGlobalsFunc):
    def __init__(self, gubun, qlist, dict_set):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, receivQ, traderQ, stgQs, liveQ
           0        1       2      3       4      5      6      7       8        9       10     11
        """
        super().__init__()
        self.gubun            = gubun
        self.windowQ          = qlist[0]
        self.teleQ            = qlist[3]
        self.straderQ         = qlist[9]
        self.stgQs            = qlist[10]
        self.stgQ             = qlist[10][self.gubun]
        self.dict_set         = dict_set
        self.indicator        = indicator

        self.buystrategy      = None
        self.sellstrategy     = None
        self.chart_code       = None
        self.arry_code        = None
        self.info_for_buy     = None
        self.info_for_sell    = None

        self.dict_data: dict[str, list] = {}
        self.dict_gj: dict[str, dict[str, int | float]] = {}
        self.dict_jg: dict[str, dict[str, int | float]] = {}
        self.dict_profit: dict[str, list] = {}

        self.dict_info        = {}
        self.dict_signal      = {}
        self.dict_buy_num     = {}
        self.dict_signal_num  = {}
        self.indi_settings    = []

        self.jgrv_count       = 0
        self.int_tujagm       = 0
        self.비중조절기준        = 0

        self.is_tick          = self.dict_set['타임프레임']
        self.avg_list         = [self.dict_set['평균값계산틱수']]
        self.buy_hj_limit     = self.dict_set['매수시장가잔량범위']
        self.sell_hj_limit    = self.dict_set['매도시장가잔량범위']
        self.sma_list         = get_ema_list(self.is_tick)
        market                = self.dict_set['거래소']
        self.market_gubun     = DICT_MARKET_GUBUN[market]
        self.market_info      = DICT_MARKET_INFO[self.market_gubun]
        self.ma_round_unit    = self.market_info['반올림단위']
        self.data_cnt         = self.market_info['데이터수'][self.is_tick]
        self.dict_findex      = self.market_info['데이터수'][self.is_tick]
        self.base_cnt         = self.dict_findex['관심종목'] + 1
        self.area_cnt         = self.dict_findex['전일비각도' if self.market_gubun == 1 else '당일거래대금각도'] + 1
        self.angle_pct_cf     = self.market_info['각도계수'][self.is_tick][0]
        self.angle_dtm_cf     = self.market_info['각도계수'][self.is_tick][1]

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

        self.ms_analyzer = MicrostructureAnalyzer(self.market_info['마켓구분'])
        self.rk_analyzer = RiskAnalyzer(self.market_info['마켓구분'])

        if self.dict_set['전략연산프로파일링']:
            import cProfile
            self.pr = cProfile.Profile()
            self.pr.enable()

    def _set_formula_data(self):
        self.fm_list, dict_fm, self.fm_tcnt = get_formula_data(False, self.data_cnt)
        self.windowQ.put((ui_num['사용자수식'], deepcopy(self.fm_list), dict_fm, self.fm_tcnt))
        if self.fm_list:
            for fm in self.fm_list:
                fm[8] = compile(fm[-2], '<string>', 'exec')

    def _update_stringategy(self):
        table_name_stg_buy      = self.market_info['매수전략디비']
        table_name_stg_sell     = self.market_info['매도전략디비']
        table_name_stg_optibuy  = self.market_info['최적화매수전략디비']
        table_name_stg_optisell = self.market_info['최적화매도전략디비']
        con  = sqlite3.connect(DB_STRATEGY)
        dfb  = pd.read_sql(f'SELECT * FROM {table_name_stg_buy}', con).set_index('index')
        dfs  = pd.read_sql(f'SELECT * FROM {table_name_stg_sell}', con).set_index('index')
        dfob = pd.read_sql(f'SELECT * FROM {table_name_stg_optibuy}', con).set_index('index')
        dfos = pd.read_sql(f'SELECT * FROM {table_name_stg_optisell}', con).set_index('index')
        con.close()

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

        if self.dict_set['매도전략'] in dfs.index:
            self.sellstrategy = compile(dfs['전략코드'][self.dict_set['매도전략']], '<string>', 'exec')
        elif self.dict_set['매도전략'] in dfos.index:
            self.sellstrategy = compile(dfos['전략코드'][self.dict_set['매도전략']], '<string>', 'exec')

        if self.dict_set['경과틱수설정']:
            def compile_condition(x):
                return compile(f'if {x}:\n    self.dict_cond_indexn[종목코드][k] = self.indexn', '<string>', 'exec')
            text_list  = self.dict_set['경과틱수설정'].split(';')
            half_cnt   = int(len(text_list) / 2)
            key_list   = text_list[:half_cnt]
            value_text_list = text_list[half_cnt:]
            value_comp_list = [compile_condition(x) for x in value_text_list]
            self.dict_condition = dict(zip(key_list, value_comp_list))

        self.set_globals_func()

    def _set_buy_strategy(self, buytxt):
        self.buystrategy, indistg = self.get_buy_indi_stg(buytxt)
        if indistg is not None:
            try:
                exec(indistg)
            except:
                self.windowQ.put((ui_num['시스템로그'], f'{format_exc()}오류 알림 - indistg'))
            else:
                self.windowQ.put((ui_num['기본로그'], f'{self.indicator}'))
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

    def _main_loop(self):
        self.windowQ.put((ui_num['기본로그'], '시스템 명령 실행 알림 - 전략 연산 시작'))
        while True:
            try:
                data = self.stgQ.get()
                if data.__class__ == list:
                    self._strategy(data)
                elif data.__class__ == tuple:
                    if self.market_gubun < 6:
                        self._update_tuple(data)
                    else:
                        self._update_tuple_future(data)
                elif data.__class__ == str:
                    self._update_string(data)
            except:
                self.windowQ.put((ui_num['시스템로그'], format_exc()))

    def _strategy(self, data):
        pass

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

    def _update_tuple_future(self, data):
        gubun, data = data
        if gubun == '잔고목록':
            self.dict_jg = data
            self.jgrv_count += 1
            if self.jgrv_count == 2:
                self.jgrv_count = 0
                self._put_gsjm_and_delete_hilo()
        elif gubun == '관심목록':
            self.dict_gj = {k: v for k, v in self.dict_gj.items() if k in data}
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
        elif gubun == '바낸선물단위정보':
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
        elif data == '프로파일링결과':
            if self.gubun == 0:
                self.windowQ.put((ui_num['시스템로그'], get_profile_text(self.pr)))
        elif data == '프로세스종료':
            time.sleep(5)
            self.windowQ.put((ui_num['기본로그'], '시스템 명령 실행 알림 - 전략연산 종료'))

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

    def Buy(self):
        취소시그널, 분할매수횟수, 매수가, 현재가, 저가대비고가등락율, 매도호가1, 매수호가1 = self.info_for_buy
        if 취소시그널:
            매수수량 = 0
        else:
            매수수량 = self._get_buy_count(분할매수횟수, 매수가, 현재가, 저가대비고가등락율)

        if '지정가' in self.dict_set['매수주문구분']:
            기준가격 = 현재가
            if self.dict_set['매수지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1
            if self.dict_set['매수지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1
            self.dict_signal['매수'].append(self.code)
            self.dict_signal_num[self.code] = self.indexn
            self.straderQ.put(('매수', self.code, 기준가격, 매수수량, now(), False))
        else:
            매수금액 = 0
            미체결수량 = 매수수량
            for 매도호가, 매도잔량 in self.shogainfo:
                if 미체결수량 - 매도잔량 <= 0:
                    매수금액 += 매도호가 * 미체결수량
                    미체결수량 -= 매도잔량
                    break
                else:
                    매수금액 += 매도호가 * 매도잔량
                    미체결수량 -= 매도잔량
            if 미체결수량 <= 0:
                if self.market_gubun < 5:
                    예상체결가 = int(매수금액 / 매수수량) if 매수수량 != 0 else 0
                elif self.market_gubun == 9:
                    소숫점자리수 = self.dict_info[self.code]['소숫점자리수']
                    예상체결가 = round(매수금액 / 매수수량, 소숫점자리수) if 매수수량 != 0 else 0
                else:
                    예상체결가 = round(매수금액 / 매수수량, 4) if 매수수량 != 0 else 0
                self.dict_signal['매수'].append(self.code)
                self.dict_signal_num[self.code] = self.indexn
                self.straderQ.put(('매수', self.code, 예상체결가, 매수수량, now(), False))

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
        if self.market_gubun < 5:
            매수수량 = int(betting / (현재가 if 매수가 == 0 else 매수가) * oc_ratio / 100)
        elif self.market_gubun == 9:
            소숫점자리수 = self.dict_info[self.code]['소숫점자리수']
            매수수량 = round(betting / (현재가 if 매수가 == 0 else 매수가) * oc_ratio / 100, 소숫점자리수)
        else:
            매수수량 = round(betting / (현재가 if 매수가 == 0 else 매수가) * oc_ratio / 100, 8)
        return 매수수량

    def Sell(self):
        취소시그널, 전량매도, 강제청산, 보유수량, 분할매도횟수, 매수가, 현재가, 저가대비고가등락율, 매도호가1, 매수호가1 = self.info_for_sell
        if 취소시그널:
            매도수량 = 0
        elif 전량매도:
            매도수량 = 보유수량
        else:
            매도수량 = self._get_sell_count(분할매도횟수, 보유수량)

        if '지정가' in self.dict_set['매도주문구분'] and not 강제청산:
            기준가격 = 현재가
            if self.dict_set['매도지정가기준가격'] == '매도1호가': 기준가격 = 매도호가1
            if self.dict_set['매도지정가기준가격'] == '매수1호가': 기준가격 = 매수호가1
            self.dict_signal['매도'].append(self.code)
            self.straderQ.put(('매도', self.code, 기준가격, 매도수량, now(), False))
        else:
            매도금액 = 0
            미체결수량 = 매도수량
            for 매수호가, 매수잔량 in self.bhogainfo:
                if 미체결수량 - 매수잔량 <= 0:
                    매도금액 += 매수호가 * 미체결수량
                    미체결수량 -= 매수잔량
                    break
                else:
                    매도금액 += 매수호가 * 매수잔량
                    미체결수량 -= 매수잔량
            if 미체결수량 <= 0:
                예상체결가 = round(매도금액 / 매도수량, self.dict_info['소숫점자리수']) if 매도수량 != 0 else 0
                self.dict_signal['매도'].append(self.code)
                self.straderQ.put(('매도', self.code, 예상체결가, 매도수량, now(), True if 강제청산 else False))

    def _get_sell_count(self, 분할매도횟수, 보유수량):
        if self.dict_set['매도분할횟수'] == 1:
            return 보유수량
        else:
            dict_ratio = dict_order_ratio[self.dict_set['매도분할방법']][self.dict_set['매도분할횟수']]
            oc_ratio = dict_ratio[분할매도횟수]
            if 분할매도횟수 == 0:
                if self.market_gubun < 5:
                    매도수량 = int(보유수량 * oc_ratio / 100)
                elif self.market_gubun == 9:
                    소숫점자리수 = self.dict_info[self.code]['소숫점자리수']
                    매도수량 = round(보유수량 * oc_ratio / 100, 소숫점자리수)
                else:
                    매도수량 = round(보유수량 * oc_ratio / 100, 8)
            else:
                보유비율 = sum(비율 for 횟수, 비율 in dict_ratio.items() if 횟수 >= 분할매도횟수)
                if self.market_gubun < 5:
                    매도수량 = int(보유수량 / 보유비율 * oc_ratio)
                elif self.market_gubun == 9:
                    소숫점자리수 = self.dict_info[self.code]['소숫점자리수']
                    매도수량 = round(보유수량 / 보유비율 * oc_ratio, 소숫점자리수)
                else:
                    매도수량 = round(보유수량 / 보유비율 * oc_ratio, 8)

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
        columns_ = self.market_info['데이터릿'][self.is_tick][:self.base_cnt]
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
