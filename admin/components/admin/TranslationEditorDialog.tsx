"use client"
import { useState } from 'react'
import { Dialog } from '@/components/ui/dialog'
import UIInput from '@/components/ui/input'
import UIButton from '@/components/ui/button'
import MarkdownEditor from './MarkdownEditor'

type Translation = { id?: string; entity: string; entity_id: string; language: string; title?: string; description?: string; content?: string; status?: string }

export default function TranslationEditorDialog({ onSaved }: { onSaved?: () => void }) {
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState<Translation>({ entity: 'guides', entity_id: '', language: 'uk', title: '', description: '', content: '', status: 'pending' })
  const [saving, setSaving] = useState(false)

  async function save() {
    setSaving(true)
    try {
      const res = await fetch('/api/translations', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      if (!res.ok) throw new Error(await res.text())
      setOpen(false); onSaved?.()
    } finally { setSaving(false) }
  }

  return (
    <div>
      <UIButton onClick={() => setOpen(true)}>Add translation</UIButton>
      <Dialog open={open} onClose={() => setOpen(false)} size="xl">
        <div className="text-lg font-medium mb-3">New translation</div>
        <div className="space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <div className="text-sm opacity-70 mb-1">Entity</div>
              <select value={form.entity} onChange={e=>setForm({ ...form, entity:e.target.value })} className="glass px-3 py-2 rounded-lg w-full">
                <option value="guides">guides</option>
                <option value="templates">templates</option>
                <option value="checklists">checklists</option>
                <option value="news">news</option>
              </select>
            </div>
            <div>
              <UIInput placeholder="Entity ID" value={form.entity_id} onChange={e=>setForm({...form, entity_id:e.target.value})}/>
            </div>
            <div>
              <div className="text-sm opacity-70 mb-1">Language</div>
              <select value={form.language} onChange={e=>setForm({ ...form, language:e.target.value })} className="glass px-3 py-2 rounded-lg w-full">
                <option value="uk">uk</option>
                <option value="ru">ru</option>
                <option value="en">en</option>
              </select>
            </div>
          </div>
          <UIInput placeholder="Title" value={form.title} onChange={e=>setForm({...form, title:e.target.value})}/>
          <UIInput placeholder="Description" value={form.description} onChange={e=>setForm({...form, description:e.target.value})}/>
          <MarkdownEditor value={form.content || ''} onChange={v=>setForm({...form, content:v})} placeholder="Translated content (Markdown)"/>
          <div className="flex items-center justify-between">
            <div className="text-xs opacity-60">Status: {form.status}</div>
            <UIButton onClick={save} disabled={saving}>{saving ? 'Saving…' : 'Save'}</UIButton>
          </div>
        </div>
      </Dialog>
    </div>
  )
}


