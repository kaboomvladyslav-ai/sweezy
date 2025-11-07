import Card from '@/components/Card'
import AppointmentsList from '@/components/admin/AppointmentsList'

export default async function AppointmentsPage() {
  return (
    <section className="space-y-8">
      <Card title="Appointments">
        <AppointmentsList/>
      </Card>
    </section>
  )
}


