"use client"
import { useEffect, useMemo, useState } from 'react'
import UIButton from '@/components/ui/button'
import UIInput from '@/components/ui/input'
import AppointmentEditorDialog from './AppointmentEditorDialog'

type Appointment = { id: string; title: string; description?: string; scheduled_at: string; duration_minutes: number; status: string }

export default function AppointmentsList() {
  const [items, setItems] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(true)
  const [q, setQ] = useState('')
  const [editing, setEditing] = useState<Appointment | undefined>(undefined)

  async function load() {
    setLoading(true)
    try {
      const res = await fetch('/api/appointments')
      if (!res.ok) { setItems([]); return }
      const data = await res.json().catch(()=>[])
      setItems(Array.isArray(data) ? data : [])
    } catch { setItems([]) } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  const filtered = useMemo(() => items.filter(t => (t.title + (t.description||'') + t.status).toLowerCase().includes(q.toLowerCase())), [items, q])

  return (
    <div className="space-y-3">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <UIInput placeholder="Search appointments…" value={q} onChange={e=>setQ(e.target.value)} className="w-full sm:max-w-xs" />
        <AppointmentEditorDialog onSaved={load} />
      </div>
      {loading ? (
        <div className="opacity-70">Loading…</div>
      ) : filtered.length === 0 ? (
        <div className="glass p-6 rounded-xl text-center opacity-80">No appointments yet.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map(t => (
            <div key={t.id} className="glass p-4 rounded-xl flex flex-col gap-2">
              <div className="text-lg font-medium">{t.title}</div>
              <div className="text-xs opacity-60">{new Date(t.scheduled_at).toLocaleString()} • {t.duration_minutes}m • {t.status}</div>
              <div className="mt-auto flex items-center justify-between">
                <UIButton variant="ghost" size="sm" onClick={() => setEditing(t)}>Edit</UIButton>
                <UIButton variant="destructive" size="sm" onClick={async () => { if (!confirm('Delete appointment?')) return; await fetch(`/api/appointments/${t.id}`, { method: 'DELETE' }); await load() }}>Delete</UIButton>
              </div>
            </div>
          ))}
        </div>
      )}
      {editing && <AppointmentEditorDialog item={editing} onSaved={() => { setEditing(undefined); load() }} />}
    </div>
  )
}


