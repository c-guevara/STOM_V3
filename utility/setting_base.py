
ICON_PATH                = './ui/icon'
STOCK_LOGIN_PATH         = './trade/stock_korea/login_kiwoom'
FUTURE_LOGIN_PATH        = './trade/future_oversea/login_future'
GRAPH_PATH               = './backtest/graph'
BACK_TEMP                = './backtest/temp'
DB_PATH                  = './_database'
DB_SETTING               = './_database/setting.db'
DB_BACKTEST              = './_database/backtest.db'
DB_TRADELIST             = './_database/tradelist.db'
DB_STRATEGY              = './_database/strategy.db'
DB_OPTUNA                = 'sqlite:///./_database/optuna.db'
DB_CODE_INFO             = './_database/code_info.db'
DB_STOCK_TICK            = './_database/stock_tick.db'
DB_STOCK_MIN             = './_database/stock_min.db'
DB_STOCK_TICK_BACK       = './_database/stock_tick_back.db'
DB_STOCK_MIN_BACK        = './_database/stock_min_back.db'
DB_STOCK_ETF_TICK        = './_database/stock_etf_tick.db'
DB_STOCK_ETF_MIN         = './_database/stock_etf_min.db'
DB_STOCK_ETF_TICK_BACK   = './_database/stock_etf_tick_back.db'
DB_STOCK_ETF_MIN_BACK    = './_database/stock_etf_min_back.db'
DB_STOCK_ETN_TICK        = './_database/stock_etn_tick.db'
DB_STOCK_ETN_MIN         = './_database/stock_etn_min.db'
DB_STOCK_ETN_TICK_BACK   = './_database/stock_etn_tick_back.db'
DB_STOCK_ETN_MIN_BACK    = './_database/stock_etn_min_back.db'
DB_STOCK_USA_TICK        = './_database/stock_usa_tick.db'
DB_STOCK_USA_MIN         = './_database/stock_usa_min.db'
DB_STOCK_USA_TICK_BACK   = './_database/stock_usa_tick_back.db'
DB_STOCK_USA_MIN_BACK    = './_database/stock_usa_min_back.db'
DB_COIN_TICK             = './_database/coin_tick.db'
DB_COIN_MIN              = './_database/coin_min.db'
DB_COIN_TICK_BACK        = './_database/coin_tick_back.db'
DB_COIN_MIN_BACK         = './_database/coin_min_back.db'
DB_FUTURE_TICK           = './_database/future_tick.db'
DB_FUTURE_MIN            = './_database/future_min.db'
DB_FUTURE_TICK_BACK      = './_database/future_tick_back.db'
DB_FUTURE_MIN_BACK       = './_database/future_min_back.db'
DB_FUTURE_NT_TICK        = './_database/future_nt_tick.db'
DB_FUTURE_NT_MIN         = './_database/future_nt_min.db'
DB_FUTURE_NT_TICK_BACK   = './_database/future_nt_tick_back.db'
DB_FUTURE_NT_MIN_BACK    = './_database/future_nt_min_back.db'
DB_FUTURE_OS_TICK        = './_database/future_os_tick.db'
DB_FUTURE_OS_MIN         = './_database/future_os_min.db'
DB_FUTURE_OS_TICK_BACK   = './_database/future_os_tick_back.db'
DB_FUTURE_OS_MIN_BACK    = './_database/future_os_min_back.db'
DB_COIN_FUTURE_TICK      = './_database/coin_future_tick.db'
DB_COIN_FUTURE_MIN       = './_database/coin_future_min.db'
DB_COIN_FUTURE_TICK_BACK = './_database/coin_future_tick_back.db'
DB_COIN_FUTURE_MIN_BACK  = './_database/coin_future_min_back.db'

ui_num = {'설정로그': 1, '종목명데이터': 2, '백테엔진': 3, '기본로그': 4, '타임로그': 5, '시스템로그': 6, '백테스트': 7,
          '사용자수식': 8, 'DB관리': 9, '실현손익': 10, '거래목록': 11, '잔고평가': 12, '잔고목록': 13,
          '체결목록': 14, '당일합계': 15, '당일상세': 16, '누적합계': 17, '누적상세': 18, '관심종목': 19,
          '호가종목': 20, '호가체결': 21, '호가잔량': 22, '호가체결2': 23, '스톰라이브1': 24, '스톰라이브2': 25, '스톰라이브3': 26,
          '스톰라이브4': 27, '스톰라이브5': 28, '스톰라이브6': 29, '스톰라이브7': 30, '스톰라이브8': 31, '스톰라이브9': 32,
          '스톰라이브10': 33, '스톰라이브11': 34, '김프': 35, '기업개요': 36, '기업공시': 37, '기업뉴스': 38, '재무년도': 39,
          '재무분기': 40, 'S상세기록': 41, 'C상세기록': 42, '차트': 43, '실시간차트': 44, '코스피': 45, '코스닥': 46, '트리맵': 47,
          '트리맵1': 48, '트리맵2': 49, '풍경사진': 50, '홈차트': 51}

columns_tt   = ['거래횟수', '총매수금액', '총매도금액', '총수익금액', '총손실금액', '수익률', '수익금합계']
columns_td   = ['종목명', '매수금액', '매도금액', '주문수량', '수익률', '수익금', '체결시간']
columns_tdf  = ['종목명', '포지션', '매수금액', '매도금액', '주문수량', '수익률', '수익금', '체결시간']
columns_tj   = ['추정예탁자산', '추정예수금', '보유종목수', '수익률', '총평가손익', '총매입금액', '총평가금액']
columns_jg   = ['종목명', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간']
columns_cj   = ['종목명', '주문구분', '주문수량', '체결수량', '미체결수량', '체결가', '체결시간', '주문가격', '주문번호']
columns_gj   = ['종목명', 'per', 'hlp', 'lhp', 'ch', 'tm', 'dm', 'bm', 'sm']
columns_jgf  = ['종목명', '포지션', '매수가', '현재가', '수익률', '평가손익', '매입금액', '평가금액', '보유수량', '분할매수횟수', '분할매도횟수', '매수시간']
columns_jgcf = columns_jgf + ['레버리지']

columns_bt   = ['종목명', '시가총액', '매수시간', '매도시간', '보유시간', '매수가', '매도가', '매수금액', '매도금액', '수익률', '수익금', '수익금합계', '매도조건', '추가매수시간']
columns_btf  = ['종목명', '포지션', '매수시간', '매도시간', '보유시간', '매수가', '매도가', '매수금액', '매도금액', '수익률', '수익금', '수익금합계', '매도조건', '추가매수시간']
columns_dt   = ['거래일자', '누적매수금액', '누적매도금액', '누적수익금액', '누적손실금액', '수익률', '누적수익금']
columns_dd   = ['체결시간', '종목명', '매수금액', '매도금액', '주문수량', '수익률', '수익금']
columns_nt   = ['기간', '누적매수금액', '누적매도금액', '누적수익금액', '누적손실금액', '누적수익률', '누적수익금']
columns_nd   = ['일자', '총매수금액', '총매도금액', '총수익금액', '총손실금액', '수익률', '수익금합계']
columns_sb   = ['구분', '백테스트', '백파인더', '최적화', '최적화V', '최적화VC', '최적화T', '최적화VT', '최적화VCT',
                '최적화OG', '최적화OGV', '최적화OGVC', '최적화OC', '최적화OCV', '최적화OCVC', '전진분석', '전진분석V', '전진분석VC', '합계']
columns_sd   = ['period', 'time', 'dc', 'at', 'bet', 'seed', 'ttc', 'atc', 'mhc', 'aht', 'pc', 'mc', 'wr', 'app', 'tpp', 'mdd', 'tsg', 'cagr']

columns_vj   = ['배팅금액', '필요자금', '거래횟수', '일평균거래횟수', '최대보유종목수', '평균보유기간', '익절', '손절',
                '승률', '평균수익률', '수익률합계', '최대낙폭률', '수익금합계', '매매성능지수', '연간예상수익률', '매수전략', '매도전략']
columns_vc   = ['변수', '배팅금액', '필요자금', '거래횟수', '일평균거래횟수', '최대보유종목수', '평균보유기간', '익절', '손절', '승률',
                '평균수익률', '수익률합계', '최대낙폭률', '수익금합계', '매매성능지수', '연간예상수익률', '매수전략', '매도전략', '범위설정']

columns_hj   = ['종목명', '현재가', '등락율', '시가총액', 'UVI', '시가', '고가', '저가']
columns_hc   = ['체결수량', '체결강도']
columns_hc2  = ['팩터구분', '팩터값']
columns_hg   = ['잔량', '호가']

columns_ns   = ['일자', '언론사', '제목', '링크']
columns_gc   = ['일자', '정보제공', '공시', '링크']
columns_jm1  = ['', '', '', '', '']
columns_jm2  = ['', '', '', '', '', '']
columns_stg1 = ['매수전략', '매도전략', '최적화매수전략', '최적화매도전략']
columns_stg2 = ['최적화범위', 'GA범위', '매수조건', '매도조건']
columns_kp   = ['종목명', '바이낸스(달러)', '업비트(원)', '대비(원)', '대비율(%)']

list_basic_tick = [
    'index', '현재가', '시가', '고가', '저가', '등락율', '당일거래대금', '체결강도', '초당매수수량', '초당매도수량',
    '초당거래대금', '고저평균대비등락율', '저가대비고가등락율', '초당매수금액', '초당매도금액',
    '당일매수금액', '최고매수금액', '최고매수가격', '당일매도금액', '최고매도금액', '최고매도가격',
    '매도호가1', '매도호가2', '매도호가3', '매도호가4', '매도호가5', '매수호가1', '매수호가2', '매수호가3', '매수호가4', '매수호가5',
    '매도잔량1', '매도잔량2', '매도잔량3', '매도잔량4', '매도잔량5', '매수잔량1', '매수잔량2', '매수잔량3', '매수잔량4', '매수잔량5',
    '매도총잔량', '매수총잔량', '매도수5호가잔량합', '관심종목',
    '이동평균60', '이동평균150', '이동평균300', '이동평균600', '이동평균1200', '최고현재가', '최저현재가',
    '체결강도평균', '최고체결강도', '최저체결강도', '최고초당매수수량', '최고초당매도수량', '누적초당매수수량',
    '누적초당매도수량', '초당거래대금평균', '등락율각도', '당일거래대금각도'
]

list_basic_min_base = [
    'index', '현재가', '시가', '고가', '저가', '등락율', '당일거래대금', '체결강도', '분당매수수량', '분당매도수량',
    '분봉시가', '분봉고가', '분봉저가',
    '분당거래대금', '고저평균대비등락율', '저가대비고가등락율', '분당매수금액', '분당매도금액',
    '당일매수금액', '최고매수금액', '최고매수가격', '당일매도금액', '최고매도금액', '최고매도가격',
    '매도호가1', '매도호가2', '매도호가3', '매도호가4', '매도호가5', '매수호가1', '매수호가2', '매수호가3', '매수호가4', '매수호가5',
    '매도잔량1', '매도잔량2', '매도잔량3', '매도잔량4', '매도잔량5', '매수잔량1', '매수잔량2', '매수잔량3', '매수잔량4', '매수잔량5',
    '매도총잔량', '매수총잔량', '매도수5호가잔량합', '관심종목',
    '이동평균5', '이동평균10', '이동평균20', '이동평균60', '이동평균120', '최고현재가', '최저현재가',
    '최고분봉고가', '최저분봉저가',
    '체결강도평균', '최고체결강도', '최저체결강도', '최고분당매수수량', '최고분당매도수량', '누적분당매수수량',
    '누적분당매도수량', '분당거래대금평균', '등락율각도', '당일거래대금각도'
]

list_stock_tick = [
    'index', '현재가', '시가', '고가', '저가', '등락율', '당일거래대금', '체결강도', '초당매수수량', '초당매도수량',
    '시가총액', '라운드피겨위5호가이내', 'VI해제시간', 'VI가격', 'VI호가단위',
    '초당거래대금', '고저평균대비등락율', '저가대비고가등락율', '초당매수금액', '초당매도금액',
    '당일매수금액', '최고매수금액', '최고매수가격', '당일매도금액', '최고매도금액', '최고매도가격',
    '매도호가1', '매도호가2', '매도호가3', '매도호가4', '매도호가5', '매수호가1', '매수호가2', '매수호가3', '매수호가4', '매수호가5',
    '매도잔량1', '매도잔량2', '매도잔량3', '매도잔량4', '매도잔량5', '매수잔량1', '매수잔량2', '매수잔량3', '매수잔량4', '매수잔량5',
    '매도총잔량', '매수총잔량', '매도수5호가잔량합', '관심종목',
    '이동평균60', '이동평균150', '이동평균300', '이동평균600', '이동평균1200', '최고현재가', '최저현재가',
    '체결강도평균', '최고체결강도', '최저체결강도', '최고초당매수수량', '최고초당매도수량', '누적초당매수수량',
    '누적초당매도수량', '초당거래대금평균', '등락율각도', '당일거래대금각도'
]

list_stock_min_base = [
    'index', '현재가', '시가', '고가', '저가', '등락율', '당일거래대금', '체결강도', '분당매수수량', '분당매도수량',
    '시가총액', '라운드피겨위5호가이내', 'VI해제시간', 'VI가격', 'VI호가단위', '분봉시가', '분봉고가', '분봉저가',
    '분당거래대금', '고저평균대비등락율', '저가대비고가등락율', '분당매수금액', '분당매도금액',
    '당일매수금액', '최고매수금액', '최고매수가격', '당일매도금액', '최고매도금액', '최고매도가격',
    '매도호가1', '매도호가2', '매도호가3', '매도호가4', '매도호가5', '매수호가1', '매수호가2', '매수호가3', '매수호가4', '매수호가5',
    '매도잔량1', '매도잔량2', '매도잔량3', '매도잔량4', '매도잔량5', '매수잔량1', '매수잔량2', '매수잔량3', '매수잔량4', '매수잔량5',
    '매도총잔량', '매수총잔량', '매도수5호가잔량합', '관심종목',
    '이동평균5', '이동평균10', '이동평균20', '이동평균60', '이동평균120', '최고현재가', '최저현재가',
    '최고분봉고가', '최저분봉저가',
    '체결강도평균', '최고체결강도', '최저체결강도', '최고분당매수수량', '최고분당매도수량', '누적분당매수수량',
    '누적분당매도수량', '분당거래대금평균', '등락율각도', '당일거래대금각도'
]

list_stockusa_tick = [
    'index', '현재가', '시가', '고가', '저가', '등락율', '당일거래대금', '체결강도', '초당매수수량', '초당매도수량',
    '시가총액', '초당거래대금', '고저평균대비등락율', '저가대비고가등락율', '초당매수금액', '초당매도금액',
    '당일매수금액', '최고매수금액', '최고매수가격', '당일매도금액', '최고매도금액', '최고매도가격',
    '매도호가1', '매도호가2', '매도호가3', '매도호가4', '매도호가5', '매수호가1', '매수호가2', '매수호가3', '매수호가4', '매수호가5',
    '매도잔량1', '매도잔량2', '매도잔량3', '매도잔량4', '매도잔량5', '매수잔량1', '매수잔량2', '매수잔량3', '매수잔량4', '매수잔량5',
    '매도총잔량', '매수총잔량', '매도수5호가잔량합', '관심종목',
    '이동평균60', '이동평균150', '이동평균300', '이동평균600', '이동평균1200', '최고현재가', '최저현재가',
    '체결강도평균', '최고체결강도', '최저체결강도', '최고초당매수수량', '최고초당매도수량', '누적초당매수수량',
    '누적초당매도수량', '초당거래대금평균', '등락율각도', '당일거래대금각도'
]

list_stockusa_min_base = [
    'index', '현재가', '시가', '고가', '저가', '등락율', '당일거래대금', '체결강도', '분당매수수량', '분당매도수량',
    '시가총액', '분봉시가', '분봉고가', '분봉저가', '분당거래대금', '고저평균대비등락율', '저가대비고가등락율', '분당매수금액', '분당매도금액',
    '당일매수금액', '최고매수금액', '최고매수가격', '당일매도금액', '최고매도금액', '최고매도가격',
    '매도호가1', '매도호가2', '매도호가3', '매도호가4', '매도호가5', '매수호가1', '매수호가2', '매수호가3', '매수호가4', '매수호가5',
    '매도잔량1', '매도잔량2', '매도잔량3', '매도잔량4', '매도잔량5', '매수잔량1', '매수잔량2', '매수잔량3', '매수잔량4', '매수잔량5',
    '매도총잔량', '매수총잔량', '매도수5호가잔량합', '관심종목',
    '이동평균5', '이동평균10', '이동평균20', '이동평균60', '이동평균120', '최고현재가', '최저현재가',
    '최고분봉고가', '최저분봉저가',
    '체결강도평균', '최고체결강도', '최저체결강도', '최고분당매수수량', '최고분당매도수량', '누적분당매수수량',
    '누적분당매도수량', '분당거래대금평균', '등락율각도', '당일거래대금각도'
]

list_chegyeol_colum1 = ['매수가', '매도가']
list_chegyeol_colum2 = ['매수가', '매도가', '매수가2', '매도가2']
list_indicator       = [
    'AD', 'ADOSC', 'ADXR', 'APO', 'AROOND', 'AROONU', 'ATR', 'BBU', 'BBM', 'BBL', 'CCI', 'DIM', 'DIP', 'MACD', 'MACDS',
    'MACDH', 'MFI', 'MOM', 'OBV', 'PPO', 'ROC', 'RSI', 'SAR', 'STOCHSK', 'STOCHSD', 'STOCHFK', 'STOCHFD', 'WILLR'
]

list_stock_min      = list_stock_min_base + list_indicator
list_basic_min      = list_basic_min_base + list_indicator
list_stockusa_min   = list_stockusa_min_base + list_indicator

list_stock_tick2    = list_stock_tick + list_chegyeol_colum1
list_basic_tick2    = list_basic_tick + list_chegyeol_colum1
list_stockusa_tick2 = list_stockusa_tick + list_chegyeol_colum1

list_stock_min2     = list_stock_min_base + list_chegyeol_colum1 + list_indicator
list_basic_min2     = list_basic_min_base + list_chegyeol_colum1 + list_indicator
list_stockusa_min2  = list_stockusa_min + list_chegyeol_colum1 + list_indicator

list_future_tick2   = list_basic_tick + list_chegyeol_colum2
list_future_min2    = list_basic_min_base + list_chegyeol_colum2 + list_indicator

DICT_MARKET_GUBUN = {
    '국내주식01': 1,
    '국내주식02': 1,
    '국내주식ETF03': 2,
    '국내주식ETF04': 2,
    '국내주식ETN05': 3,
    '국내주식ETN06': 3,
    '해외주식07': 4,
    '해외주식08': 4,
    '업비트09': 5,
    '업비트10': 5,
    '지수선물11': 6,
    '지수선물12': 6,
    '야간선물13': 7,
    '야간선물14': 7,
    '해외선물15': 8,
    '해외선물16': 8,
    '바이낸스선물17': 9,
    '바이낸스선물18': 9,
}

len_list_stock_tick    = len(list_stock_tick)
len_list_stock_min     = len(list_stock_min)
len_list_basic_tick    = len(list_basic_tick)
len_list_basic_min     = len(list_basic_min)
len_list_stockusa_tick = len(list_stockusa_tick)
len_list_stockusa_min  = len(list_stockusa_min)

DICT_MARKET_INFO = {
    1: {
        '마켓구분': 'stock', '종목디비': 'stock_info', '거래대금순위': 100, '반올림단위': 3,
        '체결디비': 'stock_chegeollist',         '잔고디비': 'stock_jangolist',
        '손익디비': 'stock_totaltradelist',      '거래디비': 'stock_tradelist',
        '매수전략디비': 'stock_buy',              '매도전략디비': 'stock_sell',
        '최적화매수전략디비': 'stock_optibuy',     '최적화매도전략디비': 'stock_optisell',
        '당일디비': {0: DB_STOCK_MIN,            1: DB_STOCK_TICK},
        '백테디비': {0: DB_STOCK_MIN_BACK,       1: DB_STOCK_TICK_BACK},
        '데이터릿': {0: list_stock_tick,         1: list_stock_min},
        '데이터수': {0: len_list_stock_tick,     1: len_list_stock_min},
        '각도계수': {0: [5, 0.01],               1: [5, 0.01]},
        '시작시간': 90000,                       '종료시간': 153500,
    },
    2: {
        '마켓구분': 'stock', '종목디비': 'stocketf_info', '거래대금순위': 10, '반올림단위': 3,
        '체결디비': 'stocketf_chegeollist',      '잔고디비': 'stocketf_jangolist',
        '손익디비': 'stocketf_totaltradelist',   '거래디비': 'stocketf_tradelist',
        '매수전략디비': 'stocketf_buy',           '매도전략디비': 'stocketf_sell',
        '최적화매수전략디비': 'stocketf_optibuy',  '최적화매도전략디비': 'stocketf_optisell',
        '당일디비': {0: DB_STOCK_ETF_MIN,        1: DB_STOCK_ETF_TICK},
        '백테디비': {0: DB_STOCK_ETF_MIN_BACK,   1: DB_STOCK_ETF_TICK_BACK},
        '데이터릿': {0: list_stock_tick,         1: list_stock_min},
        '데이터수': {0: len_list_stock_tick,     1: len_list_stock_min},
        '각도계수': {0: [5, 0.01],               1: [5, 0.01]},
        '시작시간': 90000,                       '종료시간': 153500,
    },
    3: {
        '마켓구분': 'stock', '종목디비': 'stocketn_info', '거래대금순위': 10, '반올림단위': 3,
        '체결디비': 'stocketn_chegeollist',      '잔고디비': 'stocketn_jangolist',
        '손익디비': 'stocketn_totaltradelist',   '거래디비': 'stocketn_tradelist',
        '매수전략디비': 'stocketn_buy',           '매도전략디비': 'stocketn_sell',
        '최적화매수전략디비': 'stocketn_optibuy',  '최적화매도전략디비': 'stocketn_optisell',
        '당일디비': {0: DB_STOCK_ETN_MIN,        1: DB_STOCK_ETN_TICK},
        '백테디비': {0: DB_STOCK_ETN_MIN_BACK,   1: DB_STOCK_ETN_TICK_BACK},
        '데이터릿': {0: list_stock_tick,         1: list_stock_min},
        '데이터수': {0: len_list_stock_tick,     1: len_list_stock_min},
        '각도계수': {0: [5, 0.01],               1: [5, 0.01]},
        '시작시간': 90000,                       '종료시간': 153500,
    },
    4: {
        '마켓구분': 'stock', '종목디비': 'stockusa_info', '거래대금순위': 100, '반올림단위': 3,
        '체결디비': 'stockusa_chegeollist',      '잔고디비': 'stockusa_jangolist',
        '손익디비': 'stockusa_totaltradelist',   '거래디비': 'stockusa_tradelist',
        '매수전략디비': 'stockusa_buy',           '매도전략디비': 'stockusa_sell',
        '최적화매수전략디비': 'stockusa_optibuy',  '최적화매도전략디비': 'stockusa_optisell',
        '당일디비': {0: DB_STOCK_USA_MIN,        1: DB_STOCK_USA_TICK},
        '백테디비': {0: DB_STOCK_USA_MIN_BACK,   1: DB_STOCK_USA_TICK_BACK},
        '데이터릿': {0: list_stockusa_tick,      1: list_stockusa_min},
        '데이터수': {0: len_list_stockusa_tick,  1: len_list_stockusa_min},
        '각도계수': {0: [5, 0.01],               1: [5, 0.01]},
        '시작시간': 93000,                       '종료시간': 160500,
    },
    5: {
        '마켓구분': 'coin', '종목디비': '', '거래대금순위': 10, '반올림단위': 8,
        '체결디비': 'coin_chegeollist',          '잔고디비': 'coin_jangolist',
        '손익디비': 'coin_totaltradelist',       '거래디비': 'coin_tradelist',
        '매수전략디비': 'coin_buy',               '매도전략디비': 'coin_sell',
        '최적화매수전략디비': 'coin_optibuy',      '최적화매도전략디비': 'coin_optisell',
        '당일디비': {0: DB_COIN_MIN,             1: DB_COIN_TICK},
        '백테디비': {0: DB_COIN_MIN_BACK,        1: DB_COIN_TICK_BACK},
        '데이터릿': {0: list_basic_tick,         1: list_basic_min},
        '데이터수': {0: len_list_basic_tick,     1: len_list_basic_min},
        '각도계수': {0: [10, 0.000_000_01],      1: [10, 0.000_000_01]},
        '시작시간': 0,                           '종료시간': 235030,
    },
    6: {
        '마켓구분': 'future', '종목디비': 'future_info', '거래대금순위': 100, '반올림단위': 3,
        '체결디비': 'future_chegeollist',        '잔고디비': 'future_jangolist',
        '손익디비': 'future_totaltradelist',     '거래디비': 'future_tradelist',
        '매수전략디비': 'future_buy',             '매도전략디비': 'future_sell',
        '최적화매수전략디비': 'future_optibuy',    '최적화매도전략디비': 'future_optisell',
        '당일디비': {0: DB_FUTURE_MIN,           1: DB_FUTURE_TICK},
        '백테디비': {0: DB_FUTURE_MIN_BACK,      1: DB_FUTURE_TICK_BACK},
        '데이터릿': {0: list_basic_tick,         1: list_basic_min},
        '데이터수': {0: len_list_basic_tick,     1: len_list_basic_min},
        '각도계수': {0: [100, 0.000_000_05],     1: [100, 0.000_000_05]},
        '시작시간': 84500,                       '종료시간': 155000,
    },
    7: {
        '마켓구분': 'future', '종목디비': 'futurent_info', '거래대금순위': 100, '반올림단위': 3,
        '체결디비': 'futurent_chegeollist',      '잔고디비': 'futurent_jangolist',
        '손익디비': 'futurent_totaltradelist',   '거래디비': 'futurent_tradelist',
        '당일디비': {0: DB_FUTURE_NT_MIN,        1: DB_FUTURE_NT_TICK},
        '백테디비': {0: DB_FUTURE_NT_MIN_BACK,   1: DB_FUTURE_NT_TICK_BACK},
        '데이터릿': {0: list_basic_tick,         1: list_basic_min},
        '데이터수': {0: len_list_basic_tick,     1: len_list_basic_min},
        '매수전략디비': 'futurent_buy',           '매도전략디비': 'futurent_sell',
        '최적화매수전략디비': 'futurent_optibuy',  '최적화매도전략디비': 'futurent_optisell',
        '각도계수': {0: [100, 0.000_000_05],     1: [100, 0.000_000_05]},
        '시작시간': 180000,                      '종료시간': 60500,
    },
    8: {
        '마켓구분': 'future', '종목디비': 'futureos_info', '거래대금순위': 10, '반올림단위': 3,
        '체결디비': 'futureos_chegeollist',      '잔고디비': 'futureos_jangolist',
        '손익디비': 'futureos_totaltradelist',   '거래디비': 'futureos_tradelist',
        '당일디비': {0: DB_FUTURE_OS_MIN,        1: DB_FUTURE_OS_TICK},
        '백테디비': {0: DB_FUTURE_OS_MIN_BACK,   1: DB_FUTURE_OS_TICK_BACK},
        '데이터릿': {0: list_basic_tick,         1: list_basic_min},
        '데이터수': {0: len_list_basic_tick,     1: len_list_basic_min},
        '매수전략디비': 'futureos_buy',           '매도전략전략디비': 'futureos_sell',
        '최적화매수전략디비': 'futureos_optibuy',  '최적화매도전략전략디비': 'futureos_optisell',
        '각도계수': {0: [100, 0.000_000_05],     1: [100, 0.000_000_05]},
        '시작시간': 93000,                       '종료시간': 160500,
    },
    9: {
        '마켓구분': 'coin', '종목디비': '', '거래대금순위': 10, '반올림단위': 8,
        '체결디비': 'coinfuture_chegeollist',    '잔고디비': 'coinfuture_jangolist',
        '손익디비': 'coinfuture_totaltradelist', '거래디비': 'coinfuture_tradelist',
        '당일디비': {0: DB_COIN_FUTURE_MIN,      1: DB_COIN_FUTURE_TICK},
        '백테디비': {0: DB_COIN_FUTURE_MIN_BACK, 1: DB_COIN_FUTURE_TICK_BACK},
        '데이터릿': {0: list_basic_tick,         1: list_basic_min},
        '데이터수': {0: len_list_basic_tick,     1: len_list_basic_min},
        '매수전략디비': 'coinfuture_buy',         '매도전략디비': 'coinfuture_sell',
        '최적화매수전략디비': 'coinfuture_optibuy', '최적화매도전략디비': 'coinfuture_optisell',
        '각도계수': {0: [10, 0.000_000_01],      1: [10, 0.000_000_01]},
        '시작시간': 0,                           '종료시간': 235030,
    }
}

dict_order_ratio = {
    1: {
        10: {
            0: 10.00, 1: 10.00, 2: 10.00, 3: 10.00, 4: 10.00, 5: 10.00, 6: 10.00, 7: 10.00, 8: 10.00, 9: 10.00
        },
        9: {
            0: 11.11, 1: 11.11, 2: 11.11, 3: 11.11, 4: 11.11, 5: 11.11, 6: 11.11, 7: 11.11, 8: 11.11
        },
        8: {
            0: 12.50, 1: 12.50, 2: 12.50, 3: 12.50, 4: 12.50, 5: 12.50, 6: 12.50, 7: 12.50
        },
        7: {
            0: 14.29, 1: 14.29, 2: 14.29, 3: 14.29, 4: 14.29, 5: 14.29, 6: 14.29
        },
        6: {
            0: 16.67, 1: 16.67, 2: 16.67, 3: 16.67, 4: 16.67, 5: 16.67
        },
        5: {
            0: 20.00, 1: 20.00, 2: 20.00, 3: 20.00, 4: 20.00
        },
        4: {
            0: 25.00, 1: 25.00, 2: 25.00, 3: 25.00
        },
        3: {
            0: 33.33, 1: 33.33, 2: 33.33
        },
        2: {
            0: 50.00, 1: 50.00
        },
        1: {
            0: 100.00
        }
    },
    2: {
        10: {
            0: 51.61, 1: 25.81, 2: 12.90, 3: 6.45, 4: 3.23, 5: 1.61, 6: 0.81, 7: 0.40, 8: 0.20, 9: 0.10
        },
        9: {
            0: 53.33, 1: 26.67, 2: 13.33, 3: 6.67, 4: 3.33, 5: 1.67, 6: 0.83, 7: 0.42, 8: 0.21
        },
        8: {
            0: 55.56, 1: 27.78, 2: 13.89, 3: 6.94, 4: 3.47, 5: 1.74, 6: 0.87, 7: 0.43
        },
        7: {
            0: 57.14, 1: 28.57, 2: 14.29, 3: 7.14, 4: 3.57, 5: 1.79, 6: 0.89
        },
        6: {
            0: 60.00, 1: 30.00, 2: 15.00, 3: 7.50, 4: 3.75, 5: 1.88
        },
        5: {
            0: 51.61, 1: 25.81, 2: 12.90, 3: 6.45, 4: 3.23
        },
        4: {
            0: 53.33, 1: 26.67, 2: 13.33, 3: 6.67
        },
        3: {
            0: 57.14, 1: 28.57, 2: 14.29
        },
        2: {
            0: 66.67, 1: 33.33
        },
        1: {
            0: 100.00
        }
    },
    3: {
        10: {
            0: 0.10, 1: 0.20, 2: 0.40, 3: 0.81, 4: 1.61, 5: 3.23, 6: 6.45, 7: 12.90, 8: 25.81, 9: 51.61
        },
        9: {
            0: 0.21, 1: 0.42, 2: 0.83, 3: 1.67, 4: 3.33, 5: 6.67, 6: 13.33, 7: 26.67, 8: 53.33
        },
        8: {
            0: 0.43, 1: 0.87, 2: 1.74, 3: 3.47, 4: 6.94, 5: 13.89, 6: 27.78, 7: 55.56
        },
        7: {
            0: 0.89, 1: 1.79, 2: 3.57, 3: 7.14, 4: 14.29, 5: 28.57, 6: 57.14
        },
        6: {
            0: 1.88, 1: 3.75, 2: 7.50, 3: 15.00, 4: 30.00, 5: 60.00
        },
        5: {
            0: 3.23, 1: 6.45, 2: 12.90, 3: 25.81, 4: 51.61
        },
        4: {
            0: 6.67, 1: 13.33, 2: 26.67, 3: 53.33
        },
        3: {
            0: 14.29, 1: 28.57, 2: 57.14
        },
        2: {
            0: 33.33, 1: 66.67
        },
        1: {
            0: 100.00
        }
    }
}

indi_base = {
    'ADOSC_fastperiod': 3,
    'ADOSC_slowperiod': 10,
    'ADXR_timeperiod': 14,
    'APO_fastperiod': 12,
    'APO_slowperiod': 26,
    'APO_matype': 0,
    'AROON_timeperiod': 14,
    'ATR_timeperiod': 14,
    'BBANDS_timeperiod': 5,
    'BBANDS_nbdevup': 2,
    'BBANDS_nbdevdn': 2,
    'BBANDS_matype': 0,
    'CCI_timeperiod': 14,
    'DI_timeperiod': 14,
    'MACD_fastperiod': 12,
    'MACD_slowperiod': 26,
    'MACD_signalperiod': 9,
    'MFI_timeperiod': 14,
    'MOM_timeperiod': 10,
    'PPO_fastperiod': 12,
    'PPO_slowperiod': 26,
    'PPO_matype': 0,
    'ROC_timeperiod': 10,
    'RSI_timeperiod': 14,
    'SAR_acceleration': 0.02,
    'SAR_maximum': 0.2,
    'STOCHS_fastk_period': 5,
    'STOCHS_slowk_period': 3,
    'STOCHS_slowk_matype': 0,
    'STOCHS_slowd_period': 3,
    'STOCHS_slowd_matype': 0,
    'STOCHF_fastk_period': 5,
    'STOCHF_fastd_period': 3,
    'STOCHF_fastd_matype': 0,
    'WILLR_timeperiod': 14
}

indicator = {
    'ADOSC_fastperiod': 0,
    'ADOSC_slowperiod': 0,
    'ADXR_timeperiod': 0,
    'APO_fastperiod': 0,
    'APO_slowperiod': 0,
    'APO_matype': 0,
    'AROON_timeperiod': 0,
    'ATR_timeperiod': 0,
    'BBANDS_timeperiod': 0,
    'BBANDS_nbdevup': 0,
    'BBANDS_nbdevdn': 0,
    'BBANDS_matype': 0,
    'CCI_timeperiod': 0,
    'DI_timeperiod': 0,
    'MACD_fastperiod': 0,
    'MACD_slowperiod': 0,
    'MACD_signalperiod': 0,
    'MFI_timeperiod': 0,
    'MOM_timeperiod': 0,
    'PPO_fastperiod': 0,
    'PPO_slowperiod': 0,
    'PPO_matype': 0,
    'ROC_timeperiod': 0,
    'RSI_timeperiod': 0,
    'SAR_acceleration': 0,
    'SAR_maximum': 0,
    'STOCHS_fastk_period': 0,
    'STOCHS_slowk_period': 0,
    'STOCHS_slowk_matype': 0,
    'STOCHS_slowd_period': 0,
    'STOCHS_slowd_matype': 0,
    'STOCHF_fastk_period': 0,
    'STOCHF_fastd_period': 0,
    'STOCHF_fastd_matype': 0,
    'WILLR_timeperiod': 0
}
