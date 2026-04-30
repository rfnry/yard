import {
  type Identity,
  useChatClient,
  useChatThreads,
  useQueryClient,
} from '@rfnry/chat-client-react'
import { useCallback, useTransition } from 'react'
import { buttonCls } from './ui'

type Props = {
  selectedThreadId: string | null
  onPickThread: (id: string | null) => void
  agentId: string
  identity: Identity
}

export function Sidebar({ selectedThreadId, onPickThread, agentId, identity }: Props) {
  const client = useChatClient()
  const queryClient = useQueryClient()
  const { data, isLoading } = useChatThreads({ limit: 50 })
  const [isPending, startTransition] = useTransition()
  const threads = data?.items ?? []

  const handleNewThread = useCallback(() => {
    startTransition(async () => {
      const thread = await client.createThread({ tenant: {}, clientId: crypto.randomUUID() })
      await client.addMember(thread.id, {
        role: 'assistant',
        id: agentId,
        name: 'Stock Assistant',
        metadata: {},
      })
      onPickThread(thread.id)
    })
  }, [agentId, client, onPickThread])

  const handleClear = useCallback(
    (threadId: string) => {
      void client.clearThreadEvents(threadId)
    },
    [client]
  )

  const handleDelete = useCallback(
    async (threadId: string) => {
      await client.deleteThread(threadId)
      await queryClient.invalidateQueries({ queryKey: ['chat', 'threads'] })
      if (selectedThreadId === threadId) onPickThread(null)
    },
    [client, onPickThread, queryClient, selectedThreadId]
  )

  return (
    <aside className="flex flex-col gap-3 border border-neutral-800 p-3 text-xs">
      <div className="flex items-center justify-between">
        <span className="text-neutral-500">threads</span>
        <button
          type="button"
          onClick={handleNewThread}
          disabled={isPending}
          className={buttonCls}
        >
          + new
        </button>
      </div>
      <p className="text-[10px] text-neutral-600">
        your id: <span className="text-neutral-400">{identity.id}</span>
      </p>
      <ul className="flex flex-col gap-1 overflow-auto max-h-[70vh]">
        {isLoading && <li className="text-neutral-600 italic">loading…</li>}
        {!isLoading && threads.length === 0 && (
          <li className="text-neutral-600 italic">
            no threads yet — create one or trigger /alert-user
          </li>
        )}
        {threads.map((t) => {
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
                  onClick={() => handleClear(t.id)}
                  className="text-[10px] text-neutral-500 hover:text-neutral-300"
                  title="clear thread history, keep thread"
                >
                  clear
                </button>
                <button
                  type="button"
                  onClick={() => void handleDelete(t.id)}
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
