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

  // Map `identity_id -> thread_id` for DMs. Populated on-demand by fetching
  // members for each DM thread we know about. `client.listMembers` is cheap
  // against the in-memory store used by this example.
  const [dmIndex, setDmIndex] = useState<Record<string, string>>({})

  // Derive a stable, primitive key from the set of DM thread ids so the
  // effect below re-runs only when that set actually changes (not on every
  // parent re-render).
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
            // Self-DM — key by self.
            next[identity.id] = threadId
            continue
          }
          const other = ids.find((id) => id !== identity.id)
          if (other) next[other] = threadId
        } catch {
          // Thread may have been deleted or become unreadable — skip.
        }
      }
      if (!cancelled) setDmIndex(next)
    }
    void rebuild()
    return () => {
      cancelled = true
    }
  }, [client, identity.id, dmThreadIdsKey])

  // Show self in the users list — clicking routes through `/chat/dm` with
  // `{with: self.id}`, which the server resolves to a single-member self-DM
  // (useful for jotting notes, like Slack's "You" entry). The server's
  // stable `selfdm_<id>` client_id keeps repeat clicks on the same thread.
  //
  // NB: `usePresence()` excludes the caller (server-side decision — see the
  // REST `GET /presence` handler), so we prepend self explicitly. Sorting
  // self first matches the Slack "You" placement.
  const users = useMemo<Identity[]>(
    () => [identity, ...presence.byRole.user.filter((u) => u.id !== identity.id)],
    [identity, presence.byRole.user]
  )
  const assistants = presence.byRole.assistant

  const openDm = useCallback(
    async (other: Identity) => {
      // Call the example server's `/chat/dm` endpoint. Unlike the library's
      // per-caller dedup, this endpoint matches on the DM's member set so the
      // React sidebar and the agents' `/ping-direct` webhook converge on the
      // same thread for any given (self, other) pair.
      const thread = await findOrCreateDm(serverUrl, identity, other)
      // Ensure we have a live socket subscription. joinThread is idempotent.
      await client.joinThread(thread.id)
      onPickThread(thread.id)
    },
    [client, identity, onPickThread, serverUrl]
  )

  return (
    <aside className="flex flex-col gap-4 p-3 text-xs">
      {/* Channels */}
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

      {/* Users */}
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

      {/* Assistants */}
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

// Slack-style sidebar items: no borders or backgrounds, just a text colour
// shift on hover and a subtle highlight (bold + lighter text) when selected.
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
