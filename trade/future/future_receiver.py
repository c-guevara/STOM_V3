
import sys
from PyQt5.QtWidgets import QApplication
from trade.base_receiver import BaseReceiver
from utility.static import now, error_decorator
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from trade.ls_rest_api import LsRestAPI, LsRestData, LsWebSocketReceiver


class MonitorReceivQ(QThread):
    signal1 = pyqtSignal(tuple)
    signal2 = pyqtSignal(str)

    def __init__(self, receivQ):
        super().__init__()
        self.receivQ = receivQ

    def run(self):
        while True:
            data = self.receivQ.get()
            if data.__class__ == tuple:
                self.signal1.emit(data)
            elif data.__class__ == str:
                self.signal2.emit(data)


class FutureReceiver(BaseReceiver):
    def __init__(self, qlist, dict_set, market_infos):
        super().__init__(qlist, dict_set, market_infos)

        app = QApplication(sys.argv)

        self.ls = LsRestAPI(self.windowQ, self.access, self.secret)
        self.token = self.ls.create_token()

        self._get_code_info()
        self._save_code_info_and_noti()

        self.ws_thread = LsWebSocketReceiver(self.market_info['마켓이름'], self.token, self.codes, self.windowQ)
        self.ws_thread.signal.connect(self._convert_real_data)
        self.ws_thread.start()

        self.updater = MonitorReceivQ(self.receivQ)
        self.updater.signal1.connect(self._update_tuple)
        self.updater.signal2.connect(self._sys_exit)
        self.updater.start()

        self.qtimer = QTimer()
        self.qtimer.setInterval(1 * 1000)
        self.qtimer.timeout.connect(self._scheduler)
        self.qtimer.start()

        app.exec_()

    def _get_code_info(self):
        if '지수선물' in self.dict_set['거래소']:
            self.dict_info, self.codes = self.ls.get_code_info_future()
        else:
            self.dict_info, self.codes = self.ls.get_code_info_future_night()
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

        elif tr_cd == self.tr_cd_oper:
            if body['jangubun'] == self.oper_gubun:
                operation = int(body['jstatus'])
                if operation in LsRestData.장운영상태:
                    self.operation = operation
                    self.soundQ.put(LsRestData.장운영상태[self.operation])
