import { HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export default function UIBadge({ className, ...rest }: HTMLAttributes<HTMLSpanElement>) {
  return <span className={cn('inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium bg-white/10 border border-white/15', className)} {...rest} />
}


