"use client"
import { ResponsiveContainer, LineChart, Line } from 'recharts'

type Point = { value: number }

export default function Sparkline({ data }: { data: Point[] }) {
  return (
    <div className="h-10">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <Line type="monotone" dataKey="value" stroke="#93c5fd" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}


