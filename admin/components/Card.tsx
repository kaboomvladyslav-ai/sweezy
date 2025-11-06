import { ReactNode } from 'react'

export default function Card({ title, children }: { title?: string, children: ReactNode }) {
  return (
    <div className="glass p-4">
      {title && <div className="mb-2 text-sm opacity-70">{title}</div>}
      {children}
    </div>
  )
}


