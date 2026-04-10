
from trade.base_receiver import BaseReceiver
from utility.static import now, error_decorator
from trade.ls_rest_api import LsRestAPI, WebSocketReceiver


class FutureOsReceiver(BaseReceiver):
    def __init__(self, qlist, dict_set, market_infos):
        super().__init__(qlist, dict_set, market_infos)

        self.ls = LsRestAPI(self.windowQ, self.access, self.secret)
        self.token = self.ls.create_token()

        self._get_code_info()
        self._save_code_info_and_noti()

        self.ws_thread = WebSocketReceiver(self.market_info['마켓이름'], self.token, self.codes, self.windowQ)
        self.ws_thread.signal.connect(self._convert_real_data)
        self.ws_thread.start()

    def _get_code_info(self):
        self.dict_info, self.codes = self.ls.get_code_info_future_oversea()
        self.traderQ.put(('종목정보', self.dict_info))

    @error_decorator
    def _convert_real_data(self, data):
        start = now()
        tr_cd = data['header']['tr_cd']
        body  = data['body']
        if body is None:
            return

        if tr_cd == self.tr_cd_hoga:
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

        elif tr_cd == self.tr_cd_trade:
            int_hms = int(body['trdtm'])
            if int_hms < self.market_open or self.dict_set['전략종료시간'] < int_hms:
                return
            dt = int(f"{self.str_today}{int_hms}")
            code  = body['symbol']
            c     = float(body['curpr'])
            o     = float(body['open'])
            h     = float(body['high'])
            low   = float(body['low'])
            v     = float(body['trdq'])
            per   = float(body['chgrate'])
            dm    = int(body['amount'])
            cg    = body['cgubun']
            tbids = int(body['msvolume'])
            tasks = int(body['mdvolume'])
            self._update_tick_data(dt, code, c, o, h, low, per, dm, v, cg, tbids, tasks)
