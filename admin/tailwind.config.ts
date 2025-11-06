import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#0B0E11',
          light: '#F7F7F7'
        }
      },
      boxShadow: {
        soft: '0 10px 25px -10px rgba(0,0,0,0.25)'
      },
      borderRadius: {
        xl: '1rem'
      }
    }
  },
  plugins: []
}

export default config


