import {
  type Identity,
  type Thread,
  type UserIdentity,
  useThreadActions,
  useThreadIsWorking,
  useThreadMembers,
  useThreadMetadata,
  useThreadSession,
} from '@rfnry/chat-client-react'
import { useCallback, useState } from 'react'
import { ComposerForm } from './composer'
import { EventFeed } from './ui'

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
  const isWorking = useThreadIsWorking(threadId)
  const { send } = useThreadActions(threadId)
  const members = useThreadMembers(threadId)
  const thread = useThreadMetadata(threadId)

  const [showRunEvents, setShowRunEvents] = useState(true)
  const kind = (thread?.metadata as { kind?: string } | undefined)?.kind
  const isChannel = kind === 'channel'

  const onSubmitText = useCallback(
    (trimmed: string) => {
      if (!threadId) return
      void send({
        clientId: crypto.randomUUID(),
        content: [{ type: 'text', text: trimmed }],
      })
    },
    [send, threadId]
  )

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
      <EventFeed threadId={threadId} members={members} showRunEvents={showRunEvents} />
      {isWorking && <div className="text-neutral-500 text-xs">assistant is working…</div>}
      <ComposerForm
        members={members.filter((m) => m.role === 'assistant')}
        isChannel={isChannel}
        onSubmit={onSubmitText}
      />
    </section>
  )
}
