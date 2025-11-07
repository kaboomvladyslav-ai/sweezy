import { ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'default' | 'primary' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
}

export default function UIButton({ className, variant = 'primary', size = 'md', ...rest }: Props) {
  const base = 'inline-flex items-center justify-center rounded-lg transition focus:outline-none focus:ring-2 focus:ring-white/20'
  const variants: Record<string, string> = {
    default: 'bg-white/10 hover:bg-white/15',
    primary: 'bg-gradient-to-br from-cyan-500/20 to-fuchsia-500/20 hover:from-cyan-500/30 hover:to-fuchsia-500/30 border border-white/15',
    ghost: 'bg-transparent hover:bg-white/10',
    destructive: 'bg-red-500/20 hover:bg-red-500/30',
  }
  const sizes: Record<string, string> = { sm: 'px-3 py-1.5 text-sm', md: 'px-4 py-2', lg: 'px-5 py-3 text-lg' }
  return <button className={cn(base, variants[variant], sizes[size], className)} {...rest} />
}


