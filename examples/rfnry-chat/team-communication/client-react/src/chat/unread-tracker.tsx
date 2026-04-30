import { useChatHandlers } from '@rfnry/chat-client-react'
import { useEffect } from 'react'
import { useUnread } from './unread'

/**
 * Side-effect-only component: subscribes to incoming messages and bumps
 * unread counts for any thread that isn't currently focused. Renders nothing.
 *
 * Lives in chat/ rather than at the app entry because it depends on
 * chat-event subscription primitives.
 */
export function UnreadTracker({ selectedThreadId }: { selectedThreadId: string | null }) {
  const { increment, clear } = useUnread()
  const { on } = useChatHandlers()

  // on.message default-filters self-authored events and recipient-mismatched
  // events when client.identity is set, so the only check left is "is this
  // the thread the user is currently viewing?"
  on.message((event) => {
    if (event.threadId === selectedThreadId) return
    increment(event.threadId)
  })

  useEffect(() => {
    if (selectedThreadId) clear(selectedThreadId)
  }, [selectedThreadId, clear])

  return null
}
