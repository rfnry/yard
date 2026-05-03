import { useEffect, useState } from 'react'

export type ServerSessionInfo = {
  id: string
  startedAtMs: number
}

export function useServerSessions(apiUrl: string): ServerSessionInfo[] {
  const [sessions, setSessions] = useState<ServerSessionInfo[]>([])

  useEffect(() => {
    const url = `${apiUrl.replace(/\/$/, '')}/sessions/sse`
    const es = new EventSource(url)

    es.onmessage = (ev) => {
      try {
        const payload = JSON.parse(ev.data) as {
          ids: string[]
          started_at?: Record<string, number>
        }
        const startedAt = payload.started_at ?? {}
        setSessions(
          payload.ids.map((id) => ({
            id,
            startedAtMs: startedAt[id] ?? Date.now(),
          }))
        )
      } catch {
        // ignore malformed messages
      }
    }

    return () => {
      es.close()
    }
  }, [apiUrl])

  return sessions
}
