import type { VoiceEvent } from '@rfnry/voice-protocol'
import { useEffect, useState } from 'react'

export function useSessionEvents(apiUrl: string, sessionId: string | null): VoiceEvent[] {
  const [events, setEvents] = useState<VoiceEvent[]>([])

  useEffect(() => {
    if (sessionId === null) {
      setEvents([])
      return
    }
    setEvents([])
    const url = `${apiUrl.replace(/\/$/, '')}/sessions/${encodeURIComponent(sessionId)}/events/sse`
    const es = new EventSource(url)

    es.onmessage = (ev) => {
      try {
        const parsed = JSON.parse(ev.data) as VoiceEvent
        setEvents((prev) => [...prev, parsed])
      } catch {
        // ignore malformed
      }
    }

    return () => {
      es.close()
    }
  }, [apiUrl, sessionId])

  return events
}
