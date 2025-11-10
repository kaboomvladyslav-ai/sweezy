"use client"
import { useState } from 'react'
import { Dialog } from '@/components/ui/dialog'
import Button from '@/components/ui/button'
import UIInput from '@/components/ui/input'
import UISelect from '@/components/ui/select'
import { useQueryClient } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'

export default function NewsRSSImportDialog() {
  const [open, setOpen] = useState(false)
  const [feedUrl, setFeedUrl] = useState('')
  const [language, setLanguage] = useState('uk')
  const [status, setStatus] = useState<'draft'|'published'>('draft')
  const [downloadImages, setDownloadImages] = useState(true)
  const [maxItems, setMaxItems] = useState(20)
  const [loading, setLoading] = useState(false)
  const qc = useQueryClient()

  async function submit() {
    if (!feedUrl) { toast.error('Enter RSS URL'); return }
    setLoading(true)
    try {
      const res = await fetch('/api/admin/import/news/rss', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          feed_url: feedUrl,
          language,
          status,
          max_items: maxItems,
          download_images: downloadImages,
        })
      })
      const j = await res.json().catch(()=>null)
      if (!res.ok) throw new Error(j?.detail || JSON.stringify(j) || 'Failed')
      toast.success(`Imported: ${j.created}, updated: ${j.updated}`)
      setOpen(false)
      qc.invalidateQueries({ queryKey: ['news'] })
    } catch (e: any) {
      toast.error(e?.message || 'Import failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Button onClick={()=>setOpen(true)} className="px-3 py-2">Import RSS</Button>
      <Dialog open={open} onClose={()=>setOpen(false)} size="lg">
        <div className="text-lg font-medium mb-3">Import from RSS</div>
        <div className="grid gap-3">
          <UIInput placeholder="https://example.com/feed.xml" value={feedUrl} onChange={e=>setFeedUrl(e.target.value)} />
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <div className="text-sm opacity-70 mb-1">Language</div>
              <UISelect value={language} onChange={setLanguage} options={[{value:'uk'},{value:'en'},{value:'ru'}]} />
            </div>
            <div>
              <div className="text-sm opacity-70 mb-1">Status</div>
              <UISelect value={status} onChange={(v)=>setStatus(v as any)} options={[{value:'draft'},{value:'published'}]} />
            </div>
            <div>
              <div className="text-sm opacity-70 mb-1">Max items</div>
              <UIInput type="number" value={maxItems as any} onChange={e=>setMaxItems(Number(e.target.value||20))} />
            </div>
          </div>
          <label className="inline-flex items-center gap-2 text-sm opacity-80">
            <input type="checkbox" checked={downloadImages} onChange={e=>setDownloadImages(e.target.checked)} />
            Download images to /media
          </label>
          <div className="text-right">
            <Button onClick={submit} disabled={loading || !feedUrl}>{loading ? 'Importing…' : 'Import'}</Button>
          </div>
        </div>
      </Dialog>
    </div>
  )
}


