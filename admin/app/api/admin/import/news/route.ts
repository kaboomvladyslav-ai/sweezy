import { NextRequest, NextResponse } from 'next/server'
import { serverFetch } from '@/lib/server'

export async function POST(req: NextRequest) {
  const body = await req.json()
  const res = await serverFetch('/admin/import/news', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const text = await res.text()
  return new NextResponse(text, { status: res.status })
}


