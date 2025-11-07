"use client"
import { useEffect, useMemo, useState } from 'react'
import UIButton from '@/components/ui/button'
import UIInput from '@/components/ui/input'
import TemplateEditorDialog from './TemplateEditorDialog'

type Template = { id: string; name: string; category?: string; content: string }

export default function TemplatesList() {
  const [items, setItems] = useState<Template[]>([])
  const [loading, setLoading] = useState(true)
  const [q, setQ] = useState('')
  const [editing, setEditing] = useState<Template | undefined>(undefined)

  async function load() {
    setLoading(true)
    try {
      const res = await fetch('/api/templates')
      if (!res.ok) { setItems([]); return }
      const data = await res.json().catch(()=>[])
      setItems(Array.isArray(data) ? data : [])
    } catch { setItems([]) } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  const filtered = useMemo(() => items.filter(t => (t.name + (t.category||'')).toLowerCase().includes(q.toLowerCase())), [items, q])

  return (
    <div className="space-y-3">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <UIInput placeholder="Search templates…" value={q} onChange={e=>setQ(e.target.value)} className="w-full sm:max-w-xs" />
        <div className="flex items-center gap-2">
          <input id="import-templates" type="file" accept="application/json" className="hidden" onChange={async e=>{
            const file = e.target.files?.[0]; if (!file) return
            const text = await file.text();
            try { const items = JSON.parse(text); await fetch('/api/admin/import/templates', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ items }) }); await load() } catch {}
          }}/>
          <UIButton size="sm" onClick={()=>document.getElementById('import-templates')?.click()}>Import JSON</UIButton>
          <TemplateEditorDialog onSaved={load} />
        </div>
      </div>
      {loading ? (
        <div className="opacity-70">Loading…</div>
      ) : filtered.length === 0 ? (
        <div className="glass p-6 rounded-xl text-center opacity-80">No templates yet.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(t => (
            <div key={t.id} className="glass p-4 rounded-xl flex flex-col gap-2">
              <div className="text-sm opacity-60">{t.category || '—'}</div>
              <div className="text-lg font-medium">{t.name}</div>
              <div className="mt-auto flex items-center justify-between">
                <UIButton variant="ghost" size="sm" onClick={() => setEditing(t)}>Edit</UIButton>
                <UIButton variant="destructive" size="sm" onClick={async () => { if (!confirm('Delete template?')) return; await fetch(`/api/templates/${t.id}`, { method: 'DELETE' }); await load() }}>Delete</UIButton>
              </div>
            </div>
          ))}
        </div>
      )}
      {editing && <TemplateEditorDialog item={editing} onSaved={() => { setEditing(undefined); load() }} />}
    </div>
  )
}


