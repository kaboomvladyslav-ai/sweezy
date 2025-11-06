import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: { allowedOrigins: ['localhost:5000', 'sweezy.onrender.com'] }
  }
}

export default nextConfig


