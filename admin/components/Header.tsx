"use client"
import { useTheme } from 'next-themes'
import { Sun, Moon, LogOut } from 'lucide-react'
import { logout } from '@/lib/auth'
import { usePathname } from 'next/navigation'

export default function Header() {
  const { theme, setTheme } = useTheme()
  const pathname = usePathname()
  const crumb = pathname?.split('/').filter(Boolean).slice(1).join(' / ') || 'dashboard'
  return (
    <header className="sticky top-0 z-40">
      <div className="container-grid py-4">
        <div className="glass px-4 py-2 flex items-center justify-between rounded-2xl">
          <div className="text-sm opacity-70 capitalize">{crumb}</div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
              className="glass px-3 py-2"
              aria-label="Toggle theme"
            >
              {theme === 'light' ? <Moon size={16}/> : <Sun size={16}/>}
            </button>
            <form action={logout}>
              <button className="glass px-3 py-2 flex items-center gap-2" aria-label="Logout">
                <LogOut size={16}/> Logout
              </button>
            </form>
          </div>
        </div>
      </div>
    </header>
  )
}


