import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { TradeItem } from '../types'

interface Props {
  trades: TradeItem[]
}

export default function ProfitChart({ trades }: Props) {
  const chartData = trades.map((trade, index) => ({
    index: index + 1,
    수익률: trade.수익률,
    수익금: trade.수익금
  }))

  return (
    <Card>
      <CardHeader className="p-3 md:p-6">
        <CardTitle className="text-base md:text-xl">수익률 추이</CardTitle>
      </CardHeader>
      <CardContent className="p-3 md:p-6">
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="index" tick={{ fontSize: 10 }} />
            <YAxis tick={{ fontSize: 10 }} />
            <Tooltip />
            <Line type="monotone" dataKey="수익률" stroke="#8884d8" name="수익률(%)" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="수익금" stroke="#82ca9d" name="수익금(원)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
