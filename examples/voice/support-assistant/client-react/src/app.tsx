import { useState } from 'react'
import { EventLog } from './event-log'
import { useServerSessions } from './hooks/use-server-sessions'
import { useSessionEvents } from './hooks/use-session-events'
import { Queue } from './queue'

const API_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8301'

export function App() {
  const [selected, setSelected] = useState<string | null>(null)
  const sessions = useServerSessions(API_URL)
  const events = useSessionEvents(API_URL, selected)

  return (
    <div className="app">
      <Queue apiUrl={API_URL} sessions={sessions} selectedId={selected} onSelect={setSelected} />
      <EventLog sessionId={selected} events={events} />
    </div>
  )
}
