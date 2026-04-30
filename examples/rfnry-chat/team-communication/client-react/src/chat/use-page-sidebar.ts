import {
  type AssistantIdentity,
  type Identity,
  type Thread,
  useChatClient,
  useChatPresence,
  useChatThreads,
  type UserIdentity,
} from '@rfnry/chat-client-react'
import { useCallback, useEffect, useMemo, useState } from 'react'
import { findOrCreateDm } from './dm'
import { useUnread, type UnreadMap } from './unread'

export type PageSidebarViewModel = {
  channels: Thread[]
  dmThreads: Thread[]
  users: Identity[]
  assistants: AssistantIdentity[]
  dmIndex: Record<string, string>
  unreadCounts: UnreadMap
  isHydrated: boolean
  isLoadingThreads: boolean
  openDm: (other: Identity) => Promise<void>
}

/**
 * Page-level hook for the team-communication Sidebar. Combines threads
 * + presence + DM index discovery + unread counts and exposes the
 * rendering-ready slices.
 *
 * The DM index is computed lazily by listing members of each DM thread;
 * it re-runs only when the set of DM thread ids changes.
 */
export function usePageSidebar({
  identity,
  serverUrl,
  onPickThread,
}: {
  identity: UserIdentity
  serverUrl: string
  onPickThread: (id: string | null) => void
}): PageSidebarViewModel {
  const client = useChatClient()
  const { data: threadPage, isLoading: isLoadingThreads } = useChatThreads({ limit: 50 })
  const presence = useChatPresence()
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

  return {
    channels,
    dmThreads,
    users,
    assistants,
    dmIndex,
    unreadCounts,
    isHydrated: presence.isHydrated,
    isLoadingThreads,
    openDm,
  }
}
