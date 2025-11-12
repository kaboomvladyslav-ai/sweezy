import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'
import { API_URL } from '@/lib/api'

export async function DELETE(req: NextRequest, { params }: { params: { id: string } }) {
  const token = cookies().get('access_token')?.value
  const res = await fetch(`${API_URL}/translations/glossary/${params.id}`, { method: 'DELETE', headers: token ? { Authorization: `Bearer ${token}` } : undefined })
  return new NextResponse(null, { status: res.status })
}


