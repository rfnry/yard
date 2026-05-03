import { ChatProvider, type UserIdentity } from '@rfnry/chat-client-react'
import { useMemo } from 'react'
import { Chat } from './chat'

const SERVER_URL = import.meta.env.VITE_CHAT_SERVER_URL ?? 'http://localhost:8000'

function makeGuest(): UserIdentity {
  const suffix = Math.floor(1000 + Math.random() * 9000)
  const id = `u_${crypto.randomUUID().slice(0, 8)}`
  return {
    role: 'user',
    id,
    name: `Guest-${suffix}`,
    metadata: {},
  }
}

export function App() {
  const identity = useMemo(makeGuest, [])

  return (
    <div className="min-h-screen max-w-2xl mx-auto px-6 py-8 font-mono">
      <header className="mb-4">
        <h1 className="text-xl">customer-support</h1>
        <p className="text-xs text-neutral-500 mt-1">
          each tab is a fresh guest. a new thread is opened automatically when you connect.
        </p>
        <p className="text-xs text-neutral-500 mt-1">
          you are <span className="text-neutral-200">{identity.name}</span>{' '}
          <span className="text-neutral-600">({identity.id})</span>
        </p>
      </header>

      <ChatProvider
        url={SERVER_URL}
        identity={identity}
        fallback={<p className="text-neutral-500 text-xs">Connecting…</p>}
        errorFallback={
          <p className="text-red-400 text-xs">
            Unable to reach the customer-support backend at {SERVER_URL}.
          </p>
        }
      >
        <Chat identity={identity} />
      </ChatProvider>
    </div>
  )
}
