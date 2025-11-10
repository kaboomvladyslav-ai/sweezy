"use client"
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import type { News } from '@/lib/types'
import NewsEditorDialog from './NewsEditorDialog'
import Button from '@/components/ui/button'
import UISelect from '@/components/ui/select'
import NewsRSSImportDialog from './NewsRSSImportDialog'

async function fetchNews(qs = ''): Promise<News[]> {
  try {
    const res = await fetch(`/api/news${qs}`, { cache: 'no-store' })
    if (!res.ok) return []
    return await res.json()
  } catch {
    return []
  }
}

export default function NewsList() {
  const [status, setStatus] = useState<'all'|'published'|'draft'>('all')
  const [language, setLanguage] = useState<string>('all')
  const { data = [], isLoading, refetch } = useQuery({
    queryKey: ['news', status, language],
    queryFn: () => {
      const params = new URLSearchParams()
      params.set('include_drafts', 'true')
      if (status !== 'all') params.set('status', status)
      if (language !== 'all') params.set('language', language)
      return fetchNews(`?${params.toString()}`)
    }
  })

  const onDelete = async (id: string) => {
    const res = await fetch(`/api/news/${id}`, { method: 'DELETE' })
    if (res.ok) refetch()
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-3 gap-3">
        <div className="flex items-center gap-3">
          <div className="text-sm opacity-70">Total: {data.length}</div>
          <div className="hidden sm:flex items-center gap-3">
            <span className="text-sm opacity-70">Status</span>
            <UISelect
              className="min-w-[120px]"
              value={status}
              onChange={(v)=>setStatus(v as any)}
              options={[
                { value: 'all', label: 'all' },
                { value: 'published', label: 'published' },
                { value: 'draft', label: 'draft' },
              ]}
            />
            <span className="text-sm opacity-70">Lang</span>
            <UISelect
              className="min-w-[100px]"
              value={language}
              onChange={setLanguage}
              options={[
                { value: 'all', label: 'all' },
                { value: 'uk', label: 'uk' },
                { value: 'en', label: 'en' },
                { value: 'ru', label: 'ru' },
              ]}
            />
          </div>
        </div>
        <div className="flex items-center gap-2">
          <NewsRSSImportDialog />
          <NewsEditorDialog trigger={<Button className="px-3 py-2">Create</Button>} />
        </div>
      </div>
      <div className="overflow-x-auto rounded-xl border border-white/10 bg-white/5 backdrop-blur-md shadow-soft">
        <table className="min-w-full text-sm">
          <thead className="text-left opacity-70 border-b border-white/10">
            <tr>
              <th className="py-3 px-4">Title</th>
              <th className="py-3 px-4">Source</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Date</th>
              <th className="py-3 px-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr><td className="py-6 text-center opacity-70" colSpan={4}>Loading…</td></tr>
            ) : data.length === 0 ? (
              <tr><td className="py-6 text-center opacity-70" colSpan={4}>No news yet</td></tr>
            ) : (
              data.map(item => (
                <tr key={item.id} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                  <td className="py-3 px-4">
                    <a href={item.url} target="_blank" rel="noreferrer" className="hover:underline">{item.title}</a>
                  </td>
                  <td className="py-3 px-4">{item.source}</td>
                  <td className="py-3 px-4">{(item as any).status ?? 'published'}</td>
                  <td className="py-3 px-4">{new Date(item.published_at).toLocaleDateString()}</td>
                  <td className="py-3 px-4 flex gap-2">
                    <NewsEditorDialog news={item} trigger={<Button className="px-2 py-1">Edit</Button>} />
                    <Button onClick={() => onDelete(item.id)} className="px-2 py-1 text-red-400">Delete</Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}


