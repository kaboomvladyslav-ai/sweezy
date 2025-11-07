import Card from './Card'
import UIBadge from '@/components/ui/badge'
import Sparkline from './Sparkline'
import { Users, BookOpenText, FileText, Server } from 'lucide-react'

type IconKind = 'users' | 'guides' | 'templates' | 'server'

export default function KPI({ title, value, className, icon, delta }: { title: string; value: string | number; className?: string; icon?: IconKind; delta?: number }) {
  return (
    <div className={`relative ${className ?? ''}`}>
      <div className="absolute -inset-0.5 rounded-2xl bg-gradient-to-br from-cyan-400/25 via-fuchsia-400/20 to-amber-400/20 blur-md animate-pulse" aria-hidden="true" />
      <Card title={title} className="relative">
        <div className="flex items-center justify-between">
          <div className="text-4xl font-semibold tracking-tight">{value}</div>
          <div className="opacity-70">
            {icon === 'users' && <Users size={20}/>} 
            {icon === 'guides' && <BookOpenText size={20}/>} 
            {icon === 'templates' && <FileText size={20}/>} 
            {icon === 'server' && <Server size={20}/>} 
          </div>
        </div>
        <div className="mt-2 flex items-center justify-between">
          <Sparkline data={[{value:1},{value:3},{value:2},{value:4},{value:3}]} />
          {typeof delta === 'number' && (
            <UIBadge className={delta >= 0 ? 'text-green-300' : 'text-red-300'}>
              {delta >= 0 ? '+' : ''}{delta}%
            </UIBadge>
          )}
        </div>
      </Card>
    </div>
  )
}


