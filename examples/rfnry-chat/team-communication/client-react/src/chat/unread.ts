import { createContext, useCallback, useContext, useMemo, useState } from 'react'

export type UnreadMap = Record<string, number>

type UnreadContextValue = {
  counts: UnreadMap
  increment: (threadId: string) => void
  clear: (threadId: string) => void
}

const UnreadContext = createContext<UnreadContextValue | null>(null)

export function useUnreadController(): UnreadContextValue {
  const [counts, setCounts] = useState<UnreadMap>({})
  const increment = useCallback((threadId: string) => {
    setCounts((prev) => ({ ...prev, [threadId]: (prev[threadId] ?? 0) + 1 }))
  }, [])
  const clear = useCallback((threadId: string) => {
    setCounts((prev) => {
      if (!(threadId in prev)) return prev
      const next = { ...prev }
      delete next[threadId]
      return next
    })
  }, [])
  return useMemo(() => ({ counts, increment, clear }), [counts, increment, clear])
}

export const UnreadProvider = UnreadContext.Provider

export function useUnread(): UnreadContextValue {
  const value = useContext(UnreadContext)
  if (value === null) throw new Error('useUnread must be used within an UnreadProvider')
  return value
}
