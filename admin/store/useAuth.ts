"use client"
import { create } from 'zustand'

type State = {
  accessToken: string | null
  setToken: (t: string | null) => void
}

export const useAuth = create<State>((set) => ({
  accessToken: null,
  setToken: (t) => set({ accessToken: t })
}))


