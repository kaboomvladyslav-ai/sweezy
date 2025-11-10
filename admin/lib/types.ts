export type User = {
  id: string
  email: string
  is_superuser: boolean
  created_at: string
}

export type News = {
  id: string
  title: string
  summary: string
  url: string
  source: string
  language: string
  published_at: string
  image_url?: string | null
}


