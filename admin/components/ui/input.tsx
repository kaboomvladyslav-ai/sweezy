import { InputHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

const UIInput = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(function UIInput(
  { className, ...props },
  ref
) {
  return (
    <input
      ref={ref}
      className={cn('w-full glass px-3 py-2 outline-none placeholder:opacity-60', className)}
      {...props}
    />
  )
})

export default UIInput


