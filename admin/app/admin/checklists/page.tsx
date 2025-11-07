import Card from '@/components/Card'
import ChecklistsList from '@/components/admin/ChecklistsList'

export default async function ChecklistsPage() {
  return (
    <section className="space-y-8">
      <Card title="Checklists">
        <ChecklistsList/>
      </Card>
    </section>
  )
}


