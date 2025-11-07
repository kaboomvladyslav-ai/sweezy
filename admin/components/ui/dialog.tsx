"use client"
import { ReactNode, useEffect } from 'react'
import { createPortal } from 'react-dom'
import UIButton from './button'

export function Dialog({ open, onClose, children }: { open: boolean; onClose: () => void; children: ReactNode }) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])
  if (!open) return null
  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative glass w-full max-w-md p-6">
        {children}
        <div className="mt-4 text-right">
          <UIButton variant="ghost" onClick={onClose}>Close</UIButton>
        </div>
      </div>
    </div>,
    document.body
  )
}


