import { ChatProvider, type UserIdentity } from '@rfnry/chat-client-react'
import { useMemo, useState } from 'react'
import { AlertWidget } from './alert-widget'
import { Sidebar, ThreadPanel } from './chat'

const CHAT_SERVER_URL = import.meta.env.VITE_CHAT_SERVER_URL ?? 'http://localhost:8000'
const AGENT_WEBHOOK_URL = import.meta.env.VITE_AGENT_WEBHOOK_URL ?? 'http://localhost:9100'
const AGENT_ID = 'stock-assistant'

function makeGuest(): UserIdentity {
  const id = `u_${crypto.randomUUID().slice(0, 8)}`
  return {
    role: 'user',
    id,
    name: id,
    metadata: {},
  }
}

export function App() {
  const identity = useMemo(makeGuest, [])
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null)

  return (
    <div className="min-h-screen max-w-5xl mx-auto px-6 py-6 font-mono">
      <header className="mb-4 flex items-center justify-between flex-wrap gap-2">
        <h1 className="text-xl">stock-assistant</h1>
        <p className="text-xs text-neutral-500">
          you are <span className="text-neutral-200">{identity.name}</span>{' '}
          <span className="text-neutral-600">({identity.id})</span>
        </p>
      </header>

      <ChatProvider
        url={CHAT_SERVER_URL}
        identity={identity}
        fallback={<p className="text-neutral-500 text-xs">Connecting…</p>}
        errorFallback={
          <p className="text-red-400 text-xs">
            Unable to reach the stock-assistant chat server at {CHAT_SERVER_URL}.
          </p>
        }
        onThreadInvited={(thread) => setSelectedThreadId(thread.id)}
      >
        <AlertWidget
          webhookUrl={AGENT_WEBHOOK_URL}
          defaultUserId={identity.id}
          selectedThreadId={selectedThreadId}
        />
        <div className="grid grid-cols-[260px_1fr] gap-4 mt-4">
          <Sidebar
            selectedThreadId={selectedThreadId}
            onPickThread={setSelectedThreadId}
            agentId={AGENT_ID}
            identity={identity}
          />
          <ThreadPanel
            key={selectedThreadId ?? 'none'}
            threadId={selectedThreadId}
            agentId={AGENT_ID}
          />
        </div>
      </ChatProvider>
    </div>
  )
}
