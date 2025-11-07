import Skeleton from '@/components/Skeleton'
import Card from '@/components/Card'

export default function Loading() {
  return (
    <section className="grid grid-cols-12 gap-8">
      <Card title="Status" className="col-span-12 md:col-span-4"><Skeleton className="h-10"/></Card>
      <Card title="Version" className="col-span-12 md:col-span-4"><Skeleton className="h-10"/></Card>
      <Card title="Users" className="col-span-12 md:col-span-4"><Skeleton className="h-10"/></Card>
      <Card title="Overview" className="col-span-12 xl:col-span-8"><Skeleton className="h-64"/></Card>
    </section>
  )
}


