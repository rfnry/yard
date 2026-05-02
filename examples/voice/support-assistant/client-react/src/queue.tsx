import { useEffect, useState } from 'react'
import type { ServerSessionInfo } from './hooks/use-server-sessions'

type QueueProps = {
  apiUrl: string
  sessions: ServerSessionInfo[]
  selectedId: string | null
  onSelect: (id: string) => void
}

function formatUptime(startedAtMs: number, nowMs: number): string {
  const s = Math.max(0, Math.floor((nowMs - startedAtMs) / 1000))
  if (s < 60) return `${s}s`
  const m = Math.floor(s / 60)
  const r = s % 60
  return `${m}m ${r.toString().padStart(2, '0')}s`
}

export function Queue({ apiUrl, sessions, selectedId, onSelect }: QueueProps) {
  const [now, setNow] = useState(Date.now())

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(id)
  }, [])

  const kill = async (id: string) => {
    await fetch(`${apiUrl}/sessions/${encodeURIComponent(id)}/kill`, { method: 'POST' })
  }
  const clear = async (id: string) => {
    await fetch(`${apiUrl}/sessions/${encodeURIComponent(id)}/clear`, { method: 'POST' })
  }

  return (
    <aside className="queue">
      <h1>Active calls ({sessions.length})</h1>
      {sessions.length === 0 && (
        <div className="queue-empty">no active calls. waiting for twilio…</div>
      )}
      {sessions.map((s) => (
        <button
          type="button"
          key={s.id}
          className={`queue-row ${selectedId === s.id ? 'selected' : ''}`}
          onClick={() => onSelect(s.id)}
          style={{
            display: 'block',
            width: '100%',
            textAlign: 'left',
            background: selectedId === s.id ? '#11151c' : 'transparent',
            border: `1px solid ${selectedId === s.id ? '#3b82f6' : '#1f2329'}`,
          }}
        >
          <div className="id">{s.id}</div>
          <div className="uptime">uptime {formatUptime(s.startedAtMs, now)}</div>
          <div className="actions">
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation()
                clear(s.id)
              }}
            >
              clear
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation()
                kill(s.id)
              }}
            >
              kill
            </button>
          </div>
        </button>
      ))}
    </aside>
  )
}
