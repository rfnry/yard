import {
  type Identity,
  type UserIdentity,
  useChatClient,
  useCreateThread,
  usePresence,
  useThreads,
} from '@rfnry/chat-client-react'
import { useCallback } from 'react'
import { dmClientId } from './dm'
import { buttonCls } from './ui'

type Props = {
  identity: UserIdentity
  selectedThreadId: string | null
  onPickThread: (id: string | null) => void
}

export function Sidebar({ identity, selectedThreadId, onPickThread }: Props) {
  const client = useChatClient()
  const { data: threadPage, isLoading: threadsLoading } = useThreads({ limit: 50 })
  const { mutateAsync: createThread } = useCreateThread()
  const presence = usePresence()

  const allThreads = threadPage?.items ?? []
  const channels = allThreads.filter(
    (t) => (t.metadata as { kind?: string } | undefined)?.kind === 'channel'
  )

  const users = presence.byRole.user.filter((u) => u.id !== identity.id)
  const assistants = presence.byRole.assistant

  const openDm = useCallback(
    async (other: Identity) => {
      const clientId = dmClientId(identity.id, other.id)
      // createThread is idempotent via clientId — returns the same thread on repeat call.
      const thread = await createThread({
        tenant: {},
        metadata: { kind: 'dm' },
        clientId,
      })
      // Ensure the other participant is a member (server add_member is idempotent).
      await client.addMember(thread.id, other)
      onPickThread(thread.id)
    },
    [client, createThread, identity.id, onPickThread]
  )

  return (
    <aside className="flex flex-col gap-4 border border-neutral-800 p-3 text-xs">
      {/* Channels */}
      <section className="flex flex-col gap-2">
        <span className="text-neutral-500">channels</span>
        {threadsLoading && <div className="text-neutral-600 italic">loading…</div>}
        {!threadsLoading && channels.length === 0 && (
          <div className="text-neutral-600 italic">no channels</div>
        )}
        <ul className="flex flex-col gap-1">
          {channels.map((t) => {
            const label = (t.metadata as { label?: string } | undefined)?.label ?? t.id
            const active = selectedThreadId === t.id
            return (
              <li key={t.id}>
                <button
                  type="button"
                  onClick={() => onPickThread(t.id)}
                  className={`w-full text-left px-2 py-1 border ${
                    active
                      ? 'border-neutral-200 bg-neutral-200 text-black'
                      : 'border-neutral-700 text-neutral-300 hover:border-neutral-500'
                  }`}
                >
                  # {label}
                </button>
              </li>
            )
          })}
        </ul>
      </section>

      {/* Users */}
      <section className="flex flex-col gap-2">
        <span className="text-neutral-500">users</span>
        {!presence.isHydrated && <div className="text-neutral-600 italic">loading presence…</div>}
        {presence.isHydrated && users.length === 0 && (
          <div className="text-neutral-600 italic">nobody else online</div>
        )}
        <ul className="flex flex-col gap-1">
          {users.map((u) => (
            <li key={u.id}>
              <button
                type="button"
                onClick={() => void openDm(u)}
                className={`${buttonCls} w-full text-left`}
              >
                • {u.name}
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* Assistants */}
      <section className="flex flex-col gap-2">
        <span className="text-neutral-500">assistants</span>
        {!presence.isHydrated && <div className="text-neutral-600 italic">loading presence…</div>}
        {presence.isHydrated && assistants.length === 0 && (
          <div className="text-neutral-600 italic">no agents online</div>
        )}
        <ul className="flex flex-col gap-1">
          {assistants.map((a) => (
            <li key={a.id}>
              <button
                type="button"
                onClick={() => void openDm(a)}
                className={`${buttonCls} w-full text-left`}
              >
                • {a.name}
              </button>
            </li>
          ))}
        </ul>
      </section>
    </aside>
  )
}
