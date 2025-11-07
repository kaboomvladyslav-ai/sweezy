"use client"
import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
const Chart = dynamic(() => import('./Chart'), { ssr: false })

type Point = { name: string; value: number }

export default function ChartContainer({ data }: { data: Point[] }) {
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  if (!mounted) return <div className="h-64" />
  return <Chart data={data} />
}


