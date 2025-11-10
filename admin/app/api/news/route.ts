import { NextRequest, NextResponse } from 'next/server'
import { serverFetch } from '@/lib/server'

export async function GET(req: Request) {
  const url = new URL(req.url)
  const qs = url.searchParams.toString()
  const path = qs ? `/news/?${qs}` : '/news/?limit=100'
  const res = await serverFetch(path)
  const text = await res.text()
  try {
    return new NextResponse(text, { status: res.status })
  } catch {
    return NextResponse.json({ error: 'Failed to fetch news' }, { status: 500 })
  }
}

export async function POST(req: NextRequest) {
  const body = await req.json()
  const res = await serverFetch('/news/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const text = await res.text()
  return new NextResponse(text, { status: res.status })
}


