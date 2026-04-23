import {
  type Identity,
  type Thread,
  type UserIdentity,
  useThreadActions,
  useThreadEvents,
  useThreadIsWorking,
  useThreadMembers,
  useThreadMetadata,
  useThreadSession,
} from '@rfnry/chat-client-react'
import { useCallback, useState } from 'react'
import { buttonCls, EventFeed, inputCls } from './ui'

type Props = {
  identity: UserIdentity
  threadId: string | null
}

function formatHeader(
  threadId: string,
  thread: Thread | null,
  members: Identity[],
  selfId: string
): string {
  const metadata = thread?.metadata as { kind?: string; label?: string } | undefined
  if (!metadata) return threadId
  if (metadata.kind === 'channel') {
    return `# ${metadata.label ?? threadId}`
  }
  if (metadata.kind === 'dm') {
    const other = members.find((m) => m.id !== selfId)
    return other ? `DM with ${other.name}` : 'DM'
  }
  return threadId
}

export function ThreadPanel({ identity, threadId }: Props) {
  const session = useThreadSession(threadId)
  const events = useThreadEvents(threadId)
  const isWorking = useThreadIsWorking(threadId)
  const { send } = useThreadActions(threadId)
  const members = useThreadMembers(threadId)
  const thread = useThreadMetadata(threadId)
  const [text, setText] = useState('')
  // Only surface this toggle in channels — DMs don't get noisy agent runs
  // since agents reply via user-auth'd runs scoped to the DM itself, and
  // hiding run markers in a 1:1 would be confusing rather than helpful.
  const [showRunEvents, setShowRunEvents] = useState(true)
  const kind = (thread?.metadata as { kind?: string } | undefined)?.kind
  const isChannel = kind === 'channel'

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

  if (!threadId) {
    return (
      <section className="border border-neutral-800 p-4 text-xs text-neutral-500">
        pick a channel, a user, or an assistant on the left to start.
      </section>
    )
  }
  if (session.status === 'joining') {
    return <p className="text-neutral-500 text-xs p-4">joining…</p>
  }
  if (session.status === 'error') {
    return <p className="text-red-400 text-xs p-4">error: {session.error?.message}</p>
  }

  const header = formatHeader(threadId, thread, members, identity.id)

  return (
    <section className="flex flex-col gap-3 border border-neutral-800 p-3">
      <header className="text-[10px] text-neutral-400 flex items-center gap-3">
        <span className="text-neutral-200">{header}</span>
        <span className="text-neutral-600">({threadId})</span>
        {isChannel && (
          <label className="ml-auto flex items-center gap-1 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={showRunEvents}
              onChange={(e) => setShowRunEvents(e.target.checked)}
              className="accent-neutral-200"
            />
            <span className="text-neutral-400">show run events</span>
          </label>
        )}
      </header>
      <EventFeed events={events} showRunEvents={showRunEvents} />
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
