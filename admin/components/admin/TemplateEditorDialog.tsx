"use client"
import { useEffect, useState } from 'react'
import { Dialog } from '@/components/ui/dialog'
import UIInput from '@/components/ui/input'
import UIButton from '@/components/ui/button'

type Template = { id?: string; name: string; category?: string; content: string }

export default function TemplateEditorDialog({ item, onSaved }: { item?: Template; onSaved?: () => void }) {
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState<Template>({ name: '', category: '', content: '' })
  const [saving, setSaving] = useState(false)

  useEffect(() => { if (item) setForm(item) }, [item])

  async function save() {
    setSaving(true)
    try {
      const method = item?.id ? 'PUT' : 'POST'
      const url = item?.id ? `/api/templates/${item.id}` : '/api/templates'
      const res = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      if (!res.ok) throw new Error(await res.text())
      setOpen(false)
      onSaved?.()
    } finally { setSaving(false) }
  }

  return (
    <div>
      <UIButton onClick={() => setOpen(true)}>{item ? 'Edit' : 'Create Template'}</UIButton>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <div className="text-lg font-medium mb-3">{item ? 'Edit Template' : 'Create Template'}</div>
        <div className="space-y-3">
          <UIInput placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} />
          <UIInput placeholder="Category" value={form.category} onChange={e=>setForm({...form, category:e.target.value})} />
          <textarea className="glass w-full px-3 py-2 min-h-[160px]" placeholder="Content" value={form.content} onChange={e=>setForm({...form, content:e.target.value})}/>
          <UIButton onClick={save} disabled={saving}>{saving ? 'Saving…' : 'Save'}</UIButton>
        </div>
      </Dialog>
    </div>
  )
}


