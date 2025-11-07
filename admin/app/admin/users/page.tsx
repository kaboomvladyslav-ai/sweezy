import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import DataTable from '@/components/DataTable'
import Card from '@/components/Card'
import { serverFetch } from '@/lib/server'
import UIInput from '@/components/ui/input'
import CreateUserDialog from '@/components/admin/CreateUserDialog'
import KPI from '@/components/KPI'
import { redirect } from 'next/navigation'

export default async function UsersPage() {
  const [res, statsRes] = await Promise.all([
    serverFetch('/admin/users').catch(() => null),
    serverFetch('/admin/stats').catch(()=>null)
  ])
  if (!res) {
    return (
      <section className="space-y-4">
        <h1 className="text-xl font-semibold">Users</h1>
        <Card>Failed to load users.</Card>
      </section>
    )
  }
  if (res.status === 401 || res.status === 403) {
    return (
      <section className="space-y-4">
        <Card>Unauthorized. Please login.</Card>
      </section>
    )
  }
  let users: any = []
  try { users = await res.json() } catch {}
  const stats = statsRes && statsRes.ok ? await statsRes.json().catch(()=>({counts:{}})) : {counts:{}}
  return (
    <section className="space-y-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPI title="Users" value={Array.isArray(users) ? users.length : 0} icon="users" delta={5}/>
        <KPI title="Guides" value={stats?.counts?.guides ?? 0} icon="guides" delta={2}/>
        <KPI title="Templates" value={stats?.counts?.templates ?? 0} icon="templates" delta={1}/>
        <KPI title="Server" value={'Ready'} icon="server" delta={0}/>
      </div>
      <Card>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-3">
          <UIInput placeholder="Search by email…" className="w-full sm:max-w-xs" />
          <CreateUserDialog/>
        </div>
        <DataTable data={Array.isArray(users) ? users : []}/>
      </Card>
    </section>
  )
}

function CreateUserForm() { return null }


