"use client"
import { useTheme } from 'next-themes'
import { Sun, Moon, LogOut } from 'lucide-react'
import { logout } from '@/lib/auth'

export default function Header() {
  const { theme, setTheme } = useTheme()
  return (
    <header className="flex items-center justify-between p-4">
      <div className="text-sm opacity-70">Swiss minimal dashboard</div>
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
    </header>
  )
}


