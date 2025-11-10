import Card from '@/components/Card'
import KPI from '@/components/KPI'
import { serverFetch } from '@/lib/server'
import NewsList from '@/components/admin/NewsList'

export default async function NewsPage() {
  const statsRes = await serverFetch('/admin/stats').catch(() => null)
  const stats = statsRes && statsRes.ok ? await statsRes.json().catch(() => ({ counts: {} })) : { counts: {} }

  return (
    <section className="space-y-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        <KPI title="Total News" value={stats?.counts?.news ?? 0} icon="text" delta={0} />
        <KPI title="Total Guides" value={stats?.counts?.guides ?? 0} icon="book" delta={0} />
        <KPI title="Total Templates" value={stats?.counts?.templates ?? 0} icon="fileText" delta={0} />
        <KPI title="Total Checklists" value={stats?.counts?.checklists ?? 0} icon="checkSquare" delta={0} />
        <KPI title="Server Status" value={'Ready'} icon="server" delta={0} />
      </div>
      <Card title="News">
        <NewsList />
      </Card>
    </section>
  )
}


