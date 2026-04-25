import {
  useChatClient,
  useChatStore,
  useThreadActions,
  useThreadEvents,
  useThreadIsWorking,
  useThreadSession,
} from '@rfnry/chat-client-react'
import { useCallback, useEffect, useState } from 'react'
import { buttonCls, EventFeed, inputCls } from './ui'

type Props = {
  threadId: string | null
}

export function ThreadPanel({ threadId }: Props) {
  const client = useChatClient()
  const store = useChatStore()
  const session = useThreadSession(threadId)
  const events = useThreadEvents(threadId)
  const isWorking = useThreadIsWorking(threadId)
  const { send } = useThreadActions(threadId)
  const [text, setText] = useState('')

  useEffect(() => {
    if (!threadId) return
    if (session.status !== 'joined') return
    let cancelled = false
    void (async () => {
      try {
        const page = await client.listEvents(threadId, { limit: 200 })
        if (cancelled) return
        for (const evt of page.items) {
          store.getState().actions.addEvent(evt)
        }
      } catch {}
    })()
    return () => {
      cancelled = true
    }
  }, [client, store, threadId, session.status])

  const submit = useCallback(() => {
    if (!threadId) return
    const trimmed = text.trim()
    if (!trimmed) return
    void send({
      clientId: crypto.randomUUID(),
      content: [{ type: 'text', text: trimmed }],
    })
    setText('')
  }, [send, text, threadId])

  if (!threadId)
    return (
      <section className="border border-neutral-800 p-4 text-xs text-neutral-500">
        pick a thread on the left, or start a new one.
      </section>
    )
  if (session.status === 'joining') return <p className="text-neutral-500 text-xs p-4">joining…</p>
  if (session.status === 'error')
    return <p className="text-red-400 text-xs p-4">error: {session.error?.message}</p>

  return (
    <section className="flex flex-col gap-3 border border-neutral-800 p-3">
      <header className="text-[10px] text-neutral-500">
        thread <span className="text-neutral-300">{threadId}</span>
      </header>
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
          placeholder="Say something…"
          className={inputCls}
        />
        <button type="submit" className={buttonCls}>
          send
        </button>
      </form>
    </section>
  )
}
