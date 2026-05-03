import type { VoiceEvent } from '@rfnry/voice-protocol'
import { useEffect, useRef, useState } from 'react'

type EventLogProps = {
  sessionId: string | null
  events: VoiceEvent[]
}

function classifyEvent(ev: VoiceEvent): string {
  if (ev.type.startsWith('transcript.user')) return 'user'
  if (ev.type.startsWith('transcript.agent')) return 'agent'
  if (ev.type.startsWith('tool.')) return 'tool'
  return 'lifecycle'
}

function summarize(ev: VoiceEvent): string {
  switch (ev.type) {
    case 'transcript.user.partial':
    case 'transcript.user.final':
    case 'transcript.agent.partial':
    case 'transcript.agent.final':
      return ev.text
    case 'tool.call':
      return `${ev.tool_name}(${JSON.stringify(ev.args)})`
    case 'tool.result':
      return JSON.stringify(ev.value)
    case 'session.started':
      return 'session started'
    case 'session.ended':
      return `session ended${ev.reason ? ` (${ev.reason})` : ''}`
    case 'transport.connected':
      return 'transport connected'
    case 'transport.disconnected':
      return `transport disconnected${ev.reason ? ` (${ev.reason})` : ''}`
    case 'transport.error':
      return `transport error: ${ev.error}`
    case 'interruption.detected':
      return `interruption at ${ev.position_ms}ms`
    case 'audio.spilled':
      return `audio spilled → ${ev.blob_key} (${ev.duration_ms}ms ${ev.format})`
    case 'error':
      return `error: ${ev.error}`
    default:
      return JSON.stringify(ev)
  }
}

export function EventLog({ sessionId, events }: EventLogProps) {
  const [showAudio, setShowAudio] = useState(false)
  const bottomRef = useRef<HTMLDivElement | null>(null)

  // biome-ignore lint/correctness/useExhaustiveDependencies: scroll on count change only
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [events.length])

  if (sessionId === null) {
    return (
      <main className="event-log">
        <div className="event-log header">
          <h2>event log</h2>
        </div>
        <div className="queue-empty">select a call to inspect</div>
      </main>
    )
  }

  const visible = showAudio ? events : events.filter((e) => e.type !== 'audio.spilled')

  return (
    <main className="event-log">
      <div className="header">
        <h2>{sessionId}</h2>
        <label style={{ fontSize: 11, display: 'flex', alignItems: 'center', gap: 6 }}>
          <input
            type="checkbox"
            checked={showAudio}
            onChange={(e) => setShowAudio(e.target.checked)}
          />
          show audio.spilled
        </label>
      </div>
      {visible.map((ev) => (
        <div key={ev.id} className={`event ${classifyEvent(ev)}`}>
          <div className="meta">{ev.type}</div>
          <pre>{summarize(ev)}</pre>
        </div>
      ))}
      <div ref={bottomRef} />
    </main>
  )
}
