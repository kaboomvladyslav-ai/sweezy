import Skeleton from '@/components/Skeleton'
import Card from '@/components/Card'

export default function Loading() {
  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="text-xl font-semibold">Users</div>
        <Skeleton className="h-9 w-40"/>
      </div>
      <Card>
        <Skeleton className="h-56"/>
      </Card>
    </section>
  )
}


