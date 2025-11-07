"use client"
import { useEffect, useState } from 'react'
import { Dialog } from '@/components/ui/dialog'
import UIInput from '@/components/ui/input'
import UIButton from '@/components/ui/button'

type Checklist = { id?: string; title: string; description?: string; items: string[]; is_published?: boolean }

export default function ChecklistEditorDialog({ item, onSaved }: { item?: Checklist; onSaved?: () => void }) {
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState<Checklist>({ title: '', description: '', items: [], is_published: true })
  const [itemsText, setItemsText] = useState('')
  const [saving, setSaving] = useState(false)
  useEffect(() => { if (item) { setForm(item); setItemsText(item.items.join('\n')) } }, [item])

  async function save() {
    setSaving(true)
    try {
      const method = item?.id ? 'PUT' : 'POST'
      const url = item?.id ? `/api/checklists/${item.id}` : '/api/checklists'
      const payload = { ...form, items: itemsText.split('\n').map(s=>s.trim()).filter(Boolean) }
      const res = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      if (!res.ok) throw new Error(await res.text())
      setOpen(false)
      onSaved?.()
    } finally { setSaving(false) }
  }

  return (
    <div>
      <UIButton onClick={() => setOpen(true)}>{item ? 'Edit' : 'Create Checklist'}</UIButton>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <div className="text-lg font-medium mb-3">{item ? 'Edit Checklist' : 'Create Checklist'}</div>
        <div className="space-y-3">
          <UIInput placeholder="Title" value={form.title} onChange={e=>setForm({...form, title:e.target.value})} />
          <UIInput placeholder="Description" value={form.description} onChange={e=>setForm({...form, description:e.target.value})} />
          <textarea className="glass w-full px-3 py-2 min-h-[160px]" placeholder="Items (one per line)" value={itemsText} onChange={e=>setItemsText(e.target.value)} />
          <div className="flex items-center gap-2">
            <input id="cpub" type="checkbox" checked={!!form.is_published} onChange={e=>setForm({ ...form, is_published: e.target.checked })} />
            <label htmlFor="cpub" className="text-sm opacity-80">Published</label>
          </div>
          <UIButton onClick={save} disabled={saving}>{saving ? 'Saving…' : 'Save'}</UIButton>
        </div>
      </Dialog>
    </div>
  )
}


