"use client"
import { useState } from 'react'
import { API_URL } from '@/lib/api'
import UIInput from '@/components/ui/input'
import UIButton from '@/components/ui/button'
import { Dialog } from '@/components/ui/dialog'
import { useRouter } from 'next/navigation'

export default function CreateUserDialog() {
  const [open, setOpen] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  return (
    <div>
      <UIButton onClick={() => setOpen(true)}>Create User</UIButton>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <div className="text-lg font-medium mb-3">Create User</div>
        <div className="space-y-3">
          <UIInput placeholder="Email" type="email" value={email} onChange={e=>setEmail(e.target.value)} />
          <UIInput placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
          <UIButton
            disabled={loading}
            onClick={async () => {
              setLoading(true)
              try {
                await fetch(`${API_URL}/auth/register`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ email, password })
                })
                setOpen(false)
                setEmail(''); setPassword('')
                router.refresh()
              } finally {
                setLoading(false)
              }
            }}
          >{loading ? 'Creating…' : 'Create'}</UIButton>
        </div>
      </Dialog>
    </div>
  )
}


