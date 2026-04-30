import { type Identity, useChatClient, type UserIdentity } from '@rfnry/chat-client-react'
import { useEffect, useMemo, useState } from 'react'

/**
 * Opens a brand-new thread per mounted user, adds the user and the
 * given assistant identity as members, and returns the thread id once
 * it's available. Returns `null` while the thread is still being created.
 */
export function useFreshThread(identity: UserIdentity, agent: Identity): string | null {
  const [threadId, setThreadId] = useState<string | null>(null)
  const client = useChatClient()
  const clientId = useMemo(() => crypto.randomUUID(), [])

  useEffect(() => {
    void (async () => {
      const thread = await client.createThread({ tenant: {}, clientId })
      await client.addMember(thread.id, identity)
      await client.addMember(thread.id, agent)
      setThreadId(thread.id)
    })()
  }, [client, clientId, identity, agent])

  return threadId
}
