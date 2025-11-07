"use client"
import { useState } from 'react'
import Card from '@/components/Card'
import { apiLogin } from '@/lib/api'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  return (
    <main className="container-grid min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md">
        <Card title="Admin Login">
          <form
            className="space-y-3"
            onSubmit={async (e) => {
              e.preventDefault()
              setError(null)
              setLoading(true)
              try {
                await apiLogin(email, password)
                router.replace('/admin/dashboard')
              } catch (err: any) {
                setError(err?.message || 'Login failed')
              } finally {
                setLoading(false)
              }
            }}
          >
            <input className="w-full glass px-3 py-2" placeholder="Email" type="email" value={email} onChange={e=>setEmail(e.target.value)} />
            <input className="w-full glass px-3 py-2" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
            {error && <div className="text-red-400 text-sm">{error}</div>}
            <button disabled={loading} className="w-full glass px-3 py-2 hover:bg-white/20 transition">
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>
        </Card>
      </div>
    </main>
  )
}


