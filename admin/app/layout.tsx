import './globals.css'
import type { Metadata } from 'next'
import { ReactQueryProvider } from '@/components/Providers'
import { ThemeProvider } from 'next-themes'

export const metadata: Metadata = {
  title: 'Sweezy Admin',
  description: 'Minimal admin dashboard',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html suppressHydrationWarning lang="en">
      <body className="bg-bg-light dark:bg-bg text-neutral-900 dark:text-neutral-100 antialiased">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <ReactQueryProvider>
            {children}
          </ReactQueryProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}


