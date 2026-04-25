import {
  type Identity,
  type UserIdentity,
  useChatClient,
  usePresence,
  useThreads,
} from '@rfnry/chat-client-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { findOrCreateDm } from './dm'
import { useUnread } from './unread'

type Props = {
  identity: UserIdentity
  serverUrl: string
  selectedThreadId: string | null
  onPickThread: (id: string | null) => void
}

export function Sidebar({ identity, serverUrl, selectedThreadId, onPickThread }: Props) {
  const client = useChatClient()
  const { data: threadPage, isLoading: threadsLoading } = useThreads({ limit: 50 })
  const presence = usePresence()
  const { counts: unreadCounts } = useUnread()

  const allThreads = threadPage?.items ?? []
  const channels = allThreads.filter(
    (t) => (t.metadata as { kind?: string } | undefined)?.kind === 'channel'
  )
  const dmThreads = allThreads.filter(
    (t) => (t.metadata as { kind?: string } | undefined)?.kind === 'dm'
  )

  const [dmIndex, setDmIndex] = useState<Record<string, string>>({})

  const dmThreadIdsKey = useMemo(
    () =>
      dmThreads
        .map((t) => t.id)
        .sort()
        .join(','),
    [dmThreads]
  )

  useEffect(() => {
    let cancelled = false
    const threadIds = dmThreadIdsKey ? dmThreadIdsKey.split(',') : []
    async function rebuild() {
      const next: Record<string, string> = {}
      for (const threadId of threadIds) {
        try {
          const members = await client.listMembers(threadId)
          const ids = members.map((m) => m.identityId)
          if (ids.length === 1 && ids[0] === identity.id) {
            next[identity.id] = threadId
            continue
          }
          const other = ids.find((id) => id !== identity.id)
          if (other) next[other] = threadId
        } catch {}
      }
      if (!cancelled) setDmIndex(next)
    }
    void rebuild()
    return () => {
      cancelled = true
    }
  }, [client, identity.id, dmThreadIdsKey])

  const users = useMemo<Identity[]>(
    () => [identity, ...presence.byRole.user.filter((u) => u.id !== identity.id)],
    [identity, presence.byRole.user]
  )
  const assistants = presence.byRole.assistant

  const openDm = useCallback(
    async (other: Identity) => {
      const thread = await findOrCreateDm(serverUrl, identity, other)

      await client.joinThread(thread.id)
      onPickThread(thread.id)
    },
    [client, identity, onPickThread, serverUrl]
  )

  return (
    <aside className="flex flex-col gap-4 p-3 text-xs">
      <section className="flex flex-col gap-2">
        <span className="text-neutral-500 uppercase tracking-wide text-[10px]">channels</span>
        {threadsLoading && <div className="text-neutral-600 italic">loading…</div>}
        {!threadsLoading && channels.length === 0 && (
          <div className="text-neutral-600 italic">no channels</div>
        )}
        <ul className="flex flex-col">
          {channels.map((t) => {
            const label = (t.metadata as { label?: string } | undefined)?.label ?? t.id
            const active = selectedThreadId === t.id
            const unread = unreadCounts[t.id] ?? 0
            return (
              <li key={t.id}>
                <button
                  type="button"
                  onClick={() => onPickThread(t.id)}
                  className={itemCls(active)}
                >
                  <span className="flex-1 truncate">
                    <span className="text-neutral-600">#&nbsp;</span>
                    {label}
                  </span>
                  {unread > 0 && !active && <UnreadBadge count={unread} />}
                </button>
              </li>
            )
          })}
        </ul>
      </section>

      <section className="flex flex-col gap-2">
        <span className="text-neutral-500 uppercase tracking-wide text-[10px]">users</span>
        {!presence.isHydrated && <div className="text-neutral-600 italic">loading presence…</div>}
        <ul className="flex flex-col">
          {users.map((u) => {
            const dmThreadId = dmIndex[u.id]
            const unread = dmThreadId ? (unreadCounts[dmThreadId] ?? 0) : 0
            const active = dmThreadId !== undefined && dmThreadId === selectedThreadId
            const isSelf = u.id === identity.id
            return (
              <li key={u.id}>
                <button type="button" onClick={() => void openDm(u)} className={itemCls(active)}>
                  <span className="flex-1 truncate">
                    {u.name}
                    {isSelf && <span className="text-neutral-600"> (you)</span>}
                  </span>
                  {unread > 0 && !active && <UnreadBadge count={unread} />}
                </button>
              </li>
            )
          })}
        </ul>
      </section>

      <section className="flex flex-col gap-2">
        <span className="text-neutral-500 uppercase tracking-wide text-[10px]">assistants</span>
        {!presence.isHydrated && <div className="text-neutral-600 italic">loading presence…</div>}
        {presence.isHydrated && assistants.length === 0 && (
          <div className="text-neutral-600 italic">no agents online</div>
        )}
        <ul className="flex flex-col">
          {assistants.map((a) => {
            const dmThreadId = dmIndex[a.id]
            const unread = dmThreadId ? (unreadCounts[dmThreadId] ?? 0) : 0
            const active = dmThreadId !== undefined && dmThreadId === selectedThreadId
            return (
              <li key={a.id}>
                <button type="button" onClick={() => void openDm(a)} className={itemCls(active)}>
                  <span className="flex-1 truncate">{a.name}</span>
                  {unread > 0 && !active && <UnreadBadge count={unread} />}
                </button>
              </li>
            )
          })}
        </ul>
      </section>
    </aside>
  )
}

function itemCls(active: boolean): string {
  return [
    'w-full text-left px-2 py-1 flex items-center gap-2 transition-colors',
    active
      ? 'text-neutral-100 font-semibold bg-neutral-800/60'
      : 'text-neutral-400 hover:text-neutral-200',
  ].join(' ')
}

function UnreadBadge({ count }: { count: number }) {
  return (
    <span className="ml-auto inline-block rounded-full bg-red-500 text-white px-1.5 text-[10px] leading-4 min-w-4 text-center">
      {count}
    </span>
  )
}
