"use client"
import { useEffect, useState } from 'react'
import { Dialog } from '@/components/ui/dialog'
import UIInput from '@/components/ui/input'
import UIButton from '@/components/ui/button'

type Appointment = { id?: string; title: string; description?: string; scheduled_at: string; duration_minutes: number; status?: string }

export default function AppointmentEditorDialog({ item, onSaved }: { item?: Appointment; onSaved?: () => void }) {
  const [open, setOpen] = useState(false)
  const [form, setForm] = useState<Appointment>({ title: '', description: '', scheduled_at: new Date().toISOString(), duration_minutes: 30, status: 'scheduled' })
  const [saving, setSaving] = useState(false)
  useEffect(() => { if (item) setForm(item) }, [item])

  async function save() {
    setSaving(true)
    try {
      const method = item?.id ? 'PUT' : 'POST'
      const url = item?.id ? `/api/appointments/${item.id}` : '/api/appointments'
      const res = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      if (!res.ok) throw new Error(await res.text())
      setOpen(false)
      onSaved?.()
    } finally { setSaving(false) }
  }

  return (
    <div>
      <UIButton onClick={() => setOpen(true)}>{item ? 'Edit' : 'Create Appointment'}</UIButton>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <div className="text-lg font-medium mb-3">{item ? 'Edit Appointment' : 'Create Appointment'}</div>
        <div className="space-y-3">
          <UIInput placeholder="Title" value={form.title} onChange={e=>setForm({...form, title:e.target.value})} />
          <UIInput placeholder="Description" value={form.description} onChange={e=>setForm({...form, description:e.target.value})} />
          <UIInput placeholder="Scheduled at (ISO)" value={form.scheduled_at} onChange={e=>setForm({...form, scheduled_at:e.target.value})} />
          <UIInput placeholder="Duration (min)" type="number" value={form.duration_minutes as any} onChange={e=>setForm({...form, duration_minutes:Number(e.target.value)})} />
          <select className="glass w-full px-3 py-2" value={form.status} onChange={e=>setForm({...form, status:e.target.value})}>
            <option value="scheduled">scheduled</option>
            <option value="completed">completed</option>
            <option value="canceled">canceled</option>
          </select>
          <UIButton onClick={save} disabled={saving}>{saving ? 'Saving…' : 'Save'}</UIButton>
        </div>
      </Dialog>
    </div>
  )
}


