import {
  useChatClient,
  useChatHistory,
  useChatIsWorking,
  useChatSession,
} from '@rfnry/chat-client-react'
import { useCallback, useState } from 'react'
import { buttonCls, EventFeed, inputCls } from './ui'

type Props = {
  threadId: string | null
  agentId: string
}

export function ThreadPanel({ threadId, agentId }: Props) {
  const client = useChatClient()
  const session = useChatSession(threadId)
  const events = useChatHistory(threadId)
  const isWorking = useChatIsWorking(threadId)
  const [text, setText] = useState('')

  const submit = useCallback(() => {
    if (!threadId) return
    const trimmed = text.trim()
    if (!trimmed) return
    void client.sendMessage(threadId, {
      clientId: crypto.randomUUID(),
      content: [{ type: 'text', text: trimmed }],
      recipients: [agentId],
    })
    setText('')
  }, [agentId, client, text, threadId])

  if (!threadId)
    return (
      <section className="border border-neutral-800 p-4 text-xs text-neutral-500">
        pick a thread on the left, create a new one, or trigger the alert webhook to make the agent
        open one for you.
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
