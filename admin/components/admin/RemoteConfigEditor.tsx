"use client"
import { useEffect, useState } from 'react'
import UIButton from '@/components/ui/button'

export default function RemoteConfigEditor() {
  const [value, setValue] = useState('')
  const [saving, setSaving] = useState(false)

  async function load() {
    const res = await fetch('/api/remote-config')
    const j = await res.json().catch(()=>null)
    setValue(JSON.stringify(j?.flags ?? {}, null, 2))
  }
  useEffect(() => { load() }, [])

  return (
    <div className="space-y-3">
      <div className="text-sm opacity-70">Edit flags (JSON)</div>
      <textarea className="glass w-full px-3 py-2 min-h-[260px] font-mono text-sm" value={value} onChange={e=>setValue(e.target.value)} />
      <UIButton onClick={async ()=>{
        setSaving(true)
        try {
          const flags = JSON.parse(value)
          await fetch('/api/remote-config', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ flags }) })
        } finally { setSaving(false) }
      }}>{saving ? 'Saving…' : 'Save'}</UIButton>
    </div>
  )
}


