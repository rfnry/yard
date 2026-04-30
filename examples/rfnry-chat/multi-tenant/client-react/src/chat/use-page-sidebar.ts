import { type Thread, useChatClient, useChatThreads, useQueryClient } from '@rfnry/chat-client-react'
import { useCallback, useTransition } from 'react'
import type { Organization, WorkspaceId } from '../tenants'

export type PageSidebarViewModel = {
  threads: Thread[]
  isLoading: boolean
  isPending: boolean
  handleNewThread: () => void
  handleClear: (threadId: string) => void
  handleDelete: (threadId: string) => Promise<void>
}

/**
 * Page-level hook for the multi-tenant Sidebar. Owns the threads query,
 * the new-thread mutation (with `useTransition` for pending state), and
 * the clear/delete actions. The component receives a flat ViewModel and
 * focuses on rendering org/workspace/role selectors + thread list.
 *
 * Re-render cost: re-runs only when `useChatThreads` data updates or the
 * transition pending flag flips. All callbacks are stable refs.
 */
export function usePageSidebar({
  org,
  workspaceId,
  authorId,
  selectedThreadId,
  onPickThread,
}: {
  org: Organization
  workspaceId: WorkspaceId
  authorId: string
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
      const thread = await client.createThread({
        tenant: { organization: org.id, workspace: workspaceId, author: authorId },
        clientId: crypto.randomUUID(),
      })
      await client.addMember(thread.id, org.agent)
      onPickThread(thread.id)
    })
  }, [authorId, client, onPickThread, org.agent, org.id, workspaceId])

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
