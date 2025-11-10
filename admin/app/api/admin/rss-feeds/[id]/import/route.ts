import { NextResponse } from 'next/server'
import { cookies } from 'next/headers'
import { API_URL } from '@/lib/api'

export async function POST(_: Request, { params }: { params: { id: string } }) {
  const token = cookies().get('access_token')?.value
  const res = await fetch(`${API_URL}/admin/rss-feeds/${params.id}/import`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  })
  const text = await res.text()
  return new NextResponse(text, { status: res.status, headers: { 'content-type': res.headers.get('content-type') || 'application/json' } })
}


