import { ChatProvider, type UserIdentity } from '@rfnry/chat-client-react'
import { useMemo, useState } from 'react'
import {
  PingControl,
  Sidebar,
  ThreadPanel,
  UnreadProvider,
  UnreadTracker,
  useUnreadController,
} from './chat'

const SERVER_URL = import.meta.env.VITE_CHAT_SERVER_URL ?? 'http://localhost:8000'
const GUEST_KEY = 'rfnry-team-communication-guest'

function loadOrMakeGuest(): { id: string; name: string } {
  try {
    const raw = sessionStorage.getItem(GUEST_KEY)
    if (raw) {
      const parsed = JSON.parse(raw) as { id: string; name: string }
      if (parsed?.id && parsed?.name) return parsed
    }
  } catch {}
  const suffix = Math.floor(1000 + Math.random() * 9000)
  const guest = {
    id: `u_${crypto.randomUUID().slice(0, 8)}`,
    name: `Guest-${suffix}`,
  }
  try {
    sessionStorage.setItem(GUEST_KEY, JSON.stringify(guest))
  } catch {}
  return guest
}

export function App() {
  const guest = useMemo(loadOrMakeGuest, [])
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null)
  const unread = useUnreadController()

  const identity: UserIdentity = useMemo(
    () => ({
      role: 'user',
      id: guest.id,
      name: guest.name,
      metadata: { tenant: { channel: '*' } },
    }),
    [guest.id, guest.name]
  )

  return (
    <div className="min-h-screen max-w-5xl mx-auto px-6 py-6 font-mono">
      <header className="mb-4 flex items-center justify-between flex-wrap gap-2">
        <h1 className="text-xl">team-communication</h1>
        <p className="text-xs text-neutral-500">
          you are <span className="text-neutral-200">{guest.name}</span>{' '}
          <span className="text-neutral-600">({guest.id})</span>
        </p>
      </header>

      <ChatProvider
        key={guest.id}
        url={SERVER_URL}
        identity={identity}
        fallback={<p className="text-neutral-500 text-xs">Connecting…</p>}
        errorFallback={
          <p className="text-red-400 text-xs">
            Unable to reach the team-communication chat server at {SERVER_URL}.
          </p>
        }
      >
        <UnreadProvider value={unread}>
          <UnreadTracker selectedThreadId={selectedThreadId} />
          <div className="grid grid-cols-[280px_1fr] gap-4">
            <Sidebar
              identity={identity}
              serverUrl={SERVER_URL}
              selectedThreadId={selectedThreadId}
              onPickThread={setSelectedThreadId}
            />
            <ThreadPanel
              key={selectedThreadId ?? 'none'}
              identity={identity}
              threadId={selectedThreadId}
            />
          </div>
          <PingControl identity={identity} />
        </UnreadProvider>
      </ChatProvider>
    </div>
  )
}
