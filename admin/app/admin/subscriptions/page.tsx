"use client"
import { useEffect, useState } from "react"

type Row = {
  user_id: string
  email: string
  status: string
  expire_at?: string | null
  stripe_customer_id?: string | null
  stripe_subscription_id?: string | null
}

type EventRow = {
  id: string
  user_id?: string | null
  type: string
  created_at: string
}

export default function SubscriptionsPage() {
  const [rows, setRows] = useState<Row[]>([])
  const [events, setEvents] = useState<EventRow[]>([])
  const [loading, setLoading] = useState(false)

  async function load() {
    setLoading(true)
    try {
      const base = process.env.NEXT_PUBLIC_BACKEND_URL || "https://sweezy.onrender.com"
      const list = await fetch(`${base}/api/v1/admin/subscriptions`, { credentials: "include" }).then(r => r.json())
      const evs = await fetch(`${base}/api/v1/admin/subscriptions/events`, { credentials: "include" }).then(r => r.json())
      setRows(Array.isArray(list) ? list : [])
      setEvents(Array.isArray(evs) ? evs : [])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function setStatus(userId: string, status: string) {
    const base = process.env.NEXT_PUBLIC_BACKEND_URL || "https://sweezy.onrender.com"
    await fetch(`${base}/api/v1/admin/users/${userId}/subscription`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ status }),
    })
    load()
  }

  return (
    <div className="p-6 space-y-6">
      <div className="glass p-4 flex items-center justify-between">
        <div>
          <div className="text-lg font-semibold">Subscriptions</div>
          <div className="text-xs opacity-60">Stripe + manual overrides</div>
        </div>
        <button className="glass px-3 py-2 rounded-md" onClick={load}>{loading ? "..." : "Refresh"}</button>
      </div>

      <div className="glass p-0 overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="text-left opacity-70">
            <tr>
              <th className="py-2 px-4">Email</th>
              <th className="py-2 px-4">Status</th>
              <th className="py-2 px-4">Expire</th>
              <th className="py-2 px-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.user_id} className="border-t border-white/10">
                <td className="py-2 px-4">{r.email}</td>
                <td className="py-2 px-4">{r.status}</td>
                <td className="py-2 px-4">{r.expire_at ? new Date(r.expire_at).toLocaleString() : "-"}</td>
                <td className="py-2 px-4">
                  <div className="flex gap-2">
                    <button className="glass px-2 py-1 rounded-md" onClick={() => setStatus(r.user_id, "free")}>Free</button>
                    <button className="glass px-2 py-1 rounded-md" onClick={() => setStatus(r.user_id, "trial")}>Trial</button>
                    <button className="glass px-2 py-1 rounded-md" onClick={() => setStatus(r.user_id, "premium")}>Premium</button>
                  </div>
                </td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr><td className="py-6 px-4 text-sm opacity-70">No users yet.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="glass p-4">
        <div className="text-sm font-medium mb-2">Recent Stripe events</div>
        <div className="flex flex-col gap-1 max-h-[320px] overflow-auto text-xs">
          {events.map(e => (
            <div key={e.id} className="glass p-2 rounded-md flex items-center justify-between">
              <span className="opacity-80">{e.type}</span>
              <span className="opacity-60">{new Date(e.created_at).toLocaleString()}</span>
            </div>
          ))}
          {events.length === 0 && <div className="opacity-60">No events</div>}
        </div>
      </div>
    </div>
  )
}


