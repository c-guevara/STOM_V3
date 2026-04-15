import { useState, useEffect, useRef } from 'react'
import { DashboardData, MarketType } from '../types'

export function useWebSocket(market: MarketType) {
  const [data, setData] = useState<DashboardData | null>(null)
  const [connected, setConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${market}`)
    wsRef.current = ws

    ws.onopen = () => {
      setConnected(true)
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data) as DashboardData
      setData(message)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setConnected(false)
    }

    ws.onclose = () => {
      setConnected(false)
      console.log('WebSocket disconnected')
    }

    return () => {
      ws.close()
    }
  }, [market])

  return { data, connected }
}
