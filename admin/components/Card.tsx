import { ReactNode } from 'react'

export default function Card({ title, children, className }: { title?: string, children: ReactNode, className?: string }) {
  return (
    <div className={`glass p-6 md:p-8 w-full ${className ?? ''}`}>
      {title && <div className="mb-3 text-xs uppercase tracking-wide opacity-70">{title}</div>}
      {children}
    </div>
  )
}


