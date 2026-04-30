import { type Thread, useChatClient, useChatThreads, useQueryClient } from '@rfnry/chat-client-react'
import { useCallback, useTransition } from 'react'

export type PageSidebarViewModel = {
  threads: Thread[]
  isLoading: boolean
  isPending: boolean
  handleNewThread: () => void
  handleClear: (threadId: string) => void
  handleDelete: (threadId: string) => Promise<void>
}

export function usePageSidebar({
  agentId,
  selectedThreadId,
  onPickThread,
}: {
  agentId: string
  selectedThreadId: string | null
  onPickThread: (id: string | null) => void
}): PageSidebarViewModel {
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

  return { threads, isLoading, isPending, handleNewThread, handleClear, handleDelete }
}
