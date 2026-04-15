import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { JangoItem } from '../types'

interface Props {
  items: JangoItem[]
}

export default function JangoTable({ items }: Props) {
  return (
    <Card>
      <CardHeader className="p-3 md:p-6">
        <CardTitle className="text-base md:text-xl">실시간 잔고 현황</CardTitle>
      </CardHeader>
      <CardContent className="p-0 md:p-6">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="text-xs md:text-sm">종목명</TableHead>
                <TableHead className="text-xs md:text-sm">매수가</TableHead>
                <TableHead className="text-xs md:text-sm">현재가</TableHead>
                <TableHead className="text-xs md:text-sm">수익률</TableHead>
                <TableHead className="text-xs md:text-sm hidden sm:table-cell">평가손익</TableHead>
                <TableHead className="text-xs md:text-sm hidden md:table-cell">보유수량</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.index}>
                  <TableCell className="font-medium text-xs md:text-sm">{item.종목명}</TableCell>
                  <TableCell className="text-xs md:text-sm">{item.매수가.toLocaleString()}</TableCell>
                  <TableCell className="text-xs md:text-sm">{item.현재가.toLocaleString()}</TableCell>
                  <TableCell className={`text-xs md:text-sm ${item.수익률 >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {item.수익률.toFixed(2)}%
                  </TableCell>
                  <TableCell className={`text-xs md:text-sm hidden sm:table-cell ${item.평가손익 >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {item.평가손익.toLocaleString()}
                  </TableCell>
                  <TableCell className="text-xs md:text-sm hidden md:table-cell">{item.보유수량}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  )
}
