import type { Identity, UserIdentity } from '@rfnry/chat-client-react'
import { usePageSidebar } from './use-page-sidebar'

type Props = {
  identity: UserIdentity
  serverUrl: string
  selectedThreadId: string | null
  onPickThread: (id: string | null) => void
}

export function Sidebar({ identity, serverUrl, selectedThreadId, onPickThread }: Props) {
  const page = usePageSidebar({ identity, serverUrl, onPickThread })

  return (
    <aside className="flex flex-col gap-4 p-3 text-xs">
      <section className="flex flex-col gap-2">
        <span className="text-neutral-500 uppercase tracking-wide text-[10px]">channels</span>
        {page.isLoadingThreads && <div className="text-neutral-600 italic">loading…</div>}
        {!page.isLoadingThreads && page.channels.length === 0 && (
          <div className="text-neutral-600 italic">no channels</div>
        )}
        <ul className="flex flex-col">
          {page.channels.map((t) => {
            const label = (t.metadata as { label?: string } | undefined)?.label ?? t.id
            const active = selectedThreadId === t.id
            const unread = page.unreadCounts[t.id] ?? 0
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
        {!page.isHydrated && <div className="text-neutral-600 italic">loading presence…</div>}
        <ul className="flex flex-col">
          {page.users.map((u) => {
            const dmThreadId = page.dmIndex[u.id]
            const unread = dmThreadId ? (page.unreadCounts[dmThreadId] ?? 0) : 0
            const active = dmThreadId !== undefined && dmThreadId === selectedThreadId
            const isSelf = u.id === identity.id
            return (
              <li key={u.id}>
                <button
                  type="button"
                  onClick={() => void page.openDm(u)}
                  className={itemCls(active)}
                >
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
        {!page.isHydrated && <div className="text-neutral-600 italic">loading presence…</div>}
        {page.isHydrated && page.assistants.length === 0 && (
          <div className="text-neutral-600 italic">no agents online</div>
        )}
        <ul className="flex flex-col">
          {page.assistants.map((a: Identity) => {
            const dmThreadId = page.dmIndex[a.id]
            const unread = dmThreadId ? (page.unreadCounts[dmThreadId] ?? 0) : 0
            const active = dmThreadId !== undefined && dmThreadId === selectedThreadId
            return (
              <li key={a.id}>
                <button
                  type="button"
                  onClick={() => void page.openDm(a)}
                  className={itemCls(active)}
                >
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
