
from utility.static import now
from traceback import format_exc
from utility.setting_base import ui_num
from trade.base_receiver import BaseReceiver
from trade.restapi_ls import LsRestAPI, LsRestData, WebSocketReceiver


class FutureReceiver(BaseReceiver):
    def __init__(self, qlist, dict_set, market_infos):
        super().__init__(qlist, dict_set, market_infos)

        self.ls = LsRestAPI(self.windowQ, self.access, self.secret)
        self.token = self.ls.create_token()

        self._get_code_info()
        self._save_code_info()
        self._start_notification()

        self.ws_thread = WebSocketReceiver(self.market_name, self.token, self.codes, self.windowQ)
        self.ws_thread.signal.connect(self._convert_real_data)
        self.ws_thread.start()

    def _get_code_info(self):
        if '지수선물' in self.dict_set['거래소']:
            self.dict_info, self.codes = self.ls.get_code_info_future()
        else:
            self.dict_info, self.codes = self.ls.get_code_info_future_night()
        self.traderQ.put(('종목정보', self.dict_info))

    def _convert_real_data(self, data):
        start = now()
        tr_cd = data['header']['tr_cd']
        body  = data['body']
        if body is None:
            return

        if tr_cd == self.tr_cd_hoga:
            try:
                int_hms = int(body['hotime'])
                if int_hms < self.market_open or self.dict_set['전략종료시간'] < int_hms:
                    return
                dt = int(f"{self.str_today}{int_hms}")
                code = body['symbol']
                hoga_seprice = [
                    float(body['offerho1']), float(body['offerho2']), float(body['offerho3']),
                    float(body['offerho4']), float(body['offerho5'])
                ]
                hoga_buprice = [
                    float(body['bidho1']), float(body['bidho2']), float(body['bidho3']),
                    float(body['bidho4']), float(body['bidho5'])
                ]
                hoga_samount = [
                    float(body['offerrem1']), float(body['offerrem2']), float(body['offerrem3']),
                    float(body['offerrem4']), float(body['offerrem5'])
                ]
                hoga_bamount = [
                    int(body['bidrem1']), int(body['bidrem2']), int(body['bidrem3']),
                    int(body['bidrem4']), int(body['bidrem5'])
                ]
                hoga_tamount = [
                    int(body['totofferrem']), int(body['totbidrem'])
                ]
                self._update_hoga_data(dt, code, hoga_seprice, hoga_buprice, hoga_samount,
                                       hoga_bamount, hoga_tamount, start)
            except:
                self.windowQ.put((ui_num['시스템로그'], f'{format_exc()}오류 알림 - tr_cd_hoga'))

        elif tr_cd == self.tr_cd_trade:
            try:
                int_hms = int(body['chetime'])
                if int_hms < self.market_open or self.dict_set['전략종료시간'] < int_hms:
                    return
                dt = int(f"{self.str_today}{int_hms}")
                code  = body['symbol']
                c     = float(body['price'])
                o     = float(body['open'])
                h     = float(body['high'])
                low   = float(body['low'])
                v     = float(body['cvolume'])
                per   = float(body['drate'])
                dm    = int(body['value'])
                cg    = body['cgubun']
                tbids = int(body['msvolume'])
                tasks = int(body['mdvolume'])
                ch    = float(body['cpower'])
                self._update_tick_data(dt, code, c, o, h, low, per, dm, v, cg, tbids, tasks, ch)
            except:
                self.windowQ.put((ui_num['시스템로그'], f'{format_exc()}오류 알림 - tr_cd_trade'))

        elif tr_cd == self.tr_cd_oper:
            try:
                if body['jangubun'] == self.oper_gubun:
                    operation = int(body['jstatus'])
                    if operation in LsRestData.장운영상태:
                        self.operation = operation
                        self.soundQ.put(LsRestData.장운영상태[self.operation])
            except:
                self.windowQ.put((ui_num['시스템로그'], f'{format_exc()}오류 알림 - tr_cd_oper'))
