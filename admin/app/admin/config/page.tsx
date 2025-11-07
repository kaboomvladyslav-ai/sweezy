import Card from '@/components/Card'
import RemoteConfigEditor from '@/components/admin/RemoteConfigEditor'

export default async function ConfigPage() {
  return (
    <section className="space-y-8">
      <Card title="Remote Config">
        <RemoteConfigEditor/>
      </Card>
    </section>
  )
}


