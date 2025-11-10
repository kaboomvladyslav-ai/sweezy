"use client"
import { useEffect, useState } from 'react'
import { Dialog } from '@/components/ui/dialog'
import Button from '@/components/ui/button'
import UIInput from '@/components/ui/input'
import { useQueryClient } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'
import { News } from '@/lib/types'

export default function NewsEditorDialog({ news, trigger }: { news?: News; trigger?: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  const [title, setTitle] = useState(news?.title ?? '')
  const [summary, setSummary] = useState(news?.summary ?? '')
  const [url, setUrl] = useState(news?.url ?? '')
  const [source, setSource] = useState(news?.source ?? 'Sweezy')
  const [language, setLanguage] = useState(news?.language ?? 'uk')
  const [publishedAt, setPublishedAt] = useState<string>(news?.published_at ?? new Date().toISOString())
  const [imageUrl, setImageUrl] = useState(news?.image_url ?? '')
  const [loading, setLoading] = useState(false)
  const qc = useQueryClient()

  useEffect(() => {
    if (isOpen) {
      setTitle(news?.title ?? '')
      setSummary(news?.summary ?? '')
      setUrl(news?.url ?? '')
      setSource(news?.source ?? 'Sweezy')
      setLanguage(news?.language ?? 'uk')
      setPublishedAt(news?.published_at ?? new Date().toISOString())
      setImageUrl(news?.image_url ?? '')
    }
  }, [isOpen, news])

  const submit = async () => {
    setLoading(true)
    try {
      const payload = { title, summary, url, source, language, published_at: publishedAt, image_url: imageUrl || undefined }
      const res = await fetch(news ? `/api/news/${news.id}` : `/api/news`, {
        method: news ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) throw new Error(await res.text())
      toast.success(news ? 'News updated' : 'News created')
      setIsOpen(false)
      qc.invalidateQueries({ queryKey: ['news'] })
    } catch (e: any) {
      toast.error(e?.message || 'Failed to save news')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      {trigger ? (
        <span onClick={() => setIsOpen(true)}>{trigger}</span>
      ) : (
        <Button onClick={() => setIsOpen(true)}>Create News</Button>
      )}
      <Dialog open={isOpen} onClose={() => setIsOpen(false)} size="xl">
        <div className="text-lg font-medium mb-3">{news ? 'Edit News' : 'Create News'}</div>
        <div className="text-sm opacity-70 mb-4">Manage a news item that appears in What’s New.</div>
        <div className="grid gap-3 py-2">
          <UIInput label="Title" value={title} onChange={e=>setTitle(e.target.value)} />
          <UIInput label="Summary" value={summary} onChange={e=>setSummary(e.target.value)} />
          <UIInput label="URL" value={url} onChange={e=>setUrl(e.target.value)} />
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            <UIInput label="Source" value={source} onChange={e=>setSource(e.target.value)} />
            <UIInput label="Language" value={language} onChange={e=>setLanguage(e.target.value)} />
            <UIInput label="Published At (ISO)" value={publishedAt} onChange={e=>setPublishedAt(e.target.value)} />
          </div>
          <UIInput label="Image URL" value={imageUrl} onChange={e=>setImageUrl(e.target.value)} />
        </div>
        <div className="flex justify-end">
          <Button onClick={submit} disabled={loading}>{loading ? 'Saving…' : 'Save'}</Button>
        </div>
      </Dialog>
    </div>
  )
}
