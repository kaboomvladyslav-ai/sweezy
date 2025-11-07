import Skeleton from '@/components/Skeleton'
import Card from '@/components/Card'

export default function Loading() {
  return (
    <section className="grid grid-cols-12 gap-8">
      <Card title="/health" className="col-span-12 md:col-span-4"><Skeleton className="h-12"/></Card>
      <Card title="/ready" className="col-span-12 md:col-span-4"><Skeleton className="h-12"/></Card>
      <Card title="Notes" className="col-span-12"><Skeleton className="h-40"/></Card>
    </section>
  )
}


