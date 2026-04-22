import type { Identity, UserIdentity } from '@rfnry/chat-client-react'
import {
  useChatClient,
  useCreateThread,
  useThreadActions,
  useThreadEvents,
  useThreadIsWorking,
  useThreadSession,
} from '@rfnry/chat-client-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { buttonCls, EventFeed, inputCls } from './ui'

const AGENT: Identity = {
  role: 'assistant',
  id: 'cs-agent',
  name: 'Customer Support',
  metadata: {},
}

type ChatProps = {
  identity: UserIdentity
}

export function Chat({ identity }: ChatProps) {
  const threadId = useFreshThread(identity)
  const client = useChatClient()
  const session = useThreadSession(threadId)
  const events = useThreadEvents(threadId)
  const isWorking = useThreadIsWorking(threadId)
  const { send } = useThreadActions(threadId)
  const [text, setText] = useState('')

  const submit = useCallback(() => {
    if (!threadId) return
    const trimmed = text.trim()
    if (!trimmed) return
    void send({
      clientId: crypto.randomUUID(),
      content: [{ type: 'text', text: trimmed }],
      recipients: [AGENT.id],
    })
    setText('')
  }, [send, text, threadId])

  const clearHistory = useCallback(() => {
    if (!threadId) return
    void client.clearThreadEvents(threadId)
  }, [client, threadId])

  if (!threadId) return <p className="text-neutral-500 text-xs">opening thread…</p>
  if (session.status === 'joining') return <p className="text-neutral-500 text-xs">joining…</p>
  if (session.status === 'error')
    return <p className="text-red-400 text-xs">error: {session.error?.message}</p>

  return (
    <section className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <span className="text-[10px] text-neutral-600">thread {threadId}</span>
        <button
          type="button"
          onClick={clearHistory}
          className="text-xs text-neutral-500 hover:text-neutral-300"
        >
          clear history
        </button>
      </div>
      <EventFeed events={events} />
      {isWorking && <div className="text-neutral-500 text-xs">assistant is working…</div>}
      <form
        onSubmit={(e) => {
          e.preventDefault()
          submit()
        }}
        className="flex gap-2"
      >
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Say hi…"
          className={inputCls}
        />
        <button type="submit" className={buttonCls}>
          send
        </button>
      </form>
    </section>
  )
}

function useFreshThread(identity: UserIdentity): string | null {
  const [threadId, setThreadId] = useState<string | null>(null)
  const { mutateAsync: createThread } = useCreateThread()
  const client = useChatClient()
  const clientId = useMemo(() => crypto.randomUUID(), [])

  useEffect(() => {
    void (async () => {
      const thread = await createThread({ tenant: {}, clientId })
      await client.addMember(thread.id, identity)
      await client.addMember(thread.id, AGENT)
      setThreadId(thread.id)
    })()
  }, [client, clientId, createThread, identity])

  return threadId
}
