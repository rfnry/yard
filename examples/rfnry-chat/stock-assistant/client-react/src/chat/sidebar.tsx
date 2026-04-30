import type { Identity } from '@rfnry/chat-client-react'
import { buttonCls } from './ui'
import { usePageSidebar } from './use-page-sidebar'

type Props = {
  selectedThreadId: string | null
  onPickThread: (id: string | null) => void
  agentId: string
  identity: Identity
}

export function Sidebar({ selectedThreadId, onPickThread, agentId, identity }: Props) {
  const page = usePageSidebar({ agentId, selectedThreadId, onPickThread })

  return (
    <aside className="flex flex-col gap-3 border border-neutral-800 p-3 text-xs">
      <div className="flex items-center justify-between">
        <span className="text-neutral-500">threads</span>
        <button
          type="button"
          onClick={page.handleNewThread}
          disabled={page.isPending}
          className={buttonCls}
        >
          + new
        </button>
      </div>
      <p className="text-[10px] text-neutral-600">
        your id: <span className="text-neutral-400">{identity.id}</span>
      </p>
      <ul className="flex flex-col gap-1 overflow-auto max-h-[70vh]">
        {page.isLoading && <li className="text-neutral-600 italic">loading…</li>}
        {!page.isLoading && page.threads.length === 0 && (
          <li className="text-neutral-600 italic">
            no threads yet — create one or trigger /alert-user
          </li>
        )}
        {page.threads.map((t) => {
          const isSelected = selectedThreadId === t.id
          return (
            <li
              key={t.id}
              className={`border ${
                isSelected ? 'border-neutral-200' : 'border-neutral-800 hover:border-neutral-600'
              }`}
            >
              <button
                type="button"
                onClick={() => onPickThread(t.id)}
                className={`w-full text-left px-2 py-1 ${
                  isSelected ? 'text-neutral-200' : 'text-neutral-400'
                }`}
              >
                <div className="truncate">{t.id}</div>
                <div className="text-[10px] text-neutral-600">
                  {new Date(t.createdAt).toLocaleTimeString()}
                </div>
              </button>
              <div className="flex gap-1 px-2 pb-1">
                <button
                  type="button"
                  onClick={() => page.handleClear(t.id)}
                  className="text-[10px] text-neutral-500 hover:text-neutral-300"
                  title="clear thread history, keep thread"
                >
                  clear
                </button>
                <button
                  type="button"
                  onClick={() => void page.handleDelete(t.id)}
                  className="text-[10px] text-neutral-500 hover:text-red-400"
                  title="delete thread entirely"
                >
                  delete
                </button>
              </div>
            </li>
          )
        })}
      </ul>
    </aside>
  )
}
