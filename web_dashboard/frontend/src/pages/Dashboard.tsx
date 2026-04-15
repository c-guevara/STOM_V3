import { useState } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'
import { MarketType } from '../types'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import SummaryCards from '../components/SummaryCards'
import JangoTable from '../components/JangoTable'
import ChegeolTable from '../components/ChegeolTable'
import TradeTable from '../components/TradeTable'
import ProfitChart from '../components/ProfitChart'
import AlertPanel from '../components/AlertPanel'

const MARKETS: MarketType[] = ['stock', 'stock_etf', 'stock_etn', 'stock_usa', 'future', 'future_nt', 'future_os', 'coin', 'coin_future']
const MARKET_NAMES: Record<MarketType, string> = {
  stock: '국내주식',
  stock_etf: 'ETF',
  stock_etn: 'ETN',
  stock_usa: '미국주식',
  future: '선물',
  future_nt: '선물야간',
  future_os: '해외선물',
  coin: '코인',
  coin_future: '코인선물'
}

export default function Dashboard() {
  const [selectedMarket, setSelectedMarket] = useState<MarketType>('stock')
  const { data, connected } = useWebSocket(selectedMarket)

  return (
    <div className="min-h-screen bg-background p-4 md:p-6">
      <div className="max-w-7xl mx-auto space-y-4 md:space-y-6">
        모바일용 헤더
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <h1 className="text-2xl md:text-3xl font-bold">STOM 트레이딩 대시보드</h1>
          <div className="text-sm text-gray-500">
            {connected ? '● 연결됨' : '○ 연결 안됨'}
          </div>
        </div>
        
        모바일용 시장 선택 (드롭다운)
        <Tabs value={selectedMarket} onValueChange={(v) => setSelectedMarket(v as MarketType)}>
          <TabsList className="grid w-full grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 h-auto">
            {MARKETS.map((market) => (
              <TabsTrigger 
                key={market} 
                value={market}
                className="text-xs sm:text-sm py-2 px-1 md:px-3"
              >
                <span className="hidden md:inline">{MARKET_NAMES[market]}</span>
                <span className="md:hidden">{market.split('_')[0]}</span>
              </TabsTrigger>
            ))}
          </TabsList>
          
          {MARKETS.map((market) => (
            <TabsContent key={market} value={market} className="space-y-4 md:space-y-6">
              {!connected && (
                <div className="bg-yellow-100 text-yellow-800 p-3 md:p-4 rounded text-sm">
                  연결 중...
                </div>
              )}
              
              {data && (
                <>
                  요약 카드 - 모바일에서 2열, 데스크탑에서 4열
                  <SummaryCards totalTrade={data.totaltradelist} />
                  <AlertPanel alerts={data.alerts || []} />
                  
                  잔고/체결 테이블 - 모바일에서 수직 배치
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
                    <JangoTable items={data.jangolist} />
                    <ChegeolTable items={data.chegeollist} />
                  </div>
                  
                  차트 - 모바일에서 높이 축소
                  <ProfitChart trades={data.tradelist} />
                  
                  거래 테이블 - 모바일에서 스크롤 가능
                  <TradeTable items={data.tradelist} />
                </>
              )}
            </TabsContent>
          ))}
        </Tabs>
      </div>
    </div>
  )
}
