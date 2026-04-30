import {
  type ChatSession,
  type Event,
  useChatClient,
  useChatHistory,
  useChatIsWorking,
  useChatSession,
  useChatStore,
} from '@rfnry/chat-client-react'
import { useCallback, useEffect, useState } from 'react'

export type PageThreadPanelViewModel = {
  session: ChatSession
  events: Event[]
  isWorking: boolean
  text: string
  setText: (next: string) => void
  submit: () => void
}

/**
 * Page-level hook for the multi-tenant ThreadPanel. Bundles the session
 * lifecycle, history subscription, work indicator, and the send action.
 * Also runs the listEvents backfill on join to load older messages
 * outside the replay window — that side effect lives here, not in the
 * UI.
 */
export function usePageThreadPanel(threadId: string | null): PageThreadPanelViewModel {
  const client = useChatClient()
  const store = useChatStore()
  const session = useChatSession(threadId)
  const events = useChatHistory(threadId)
  const isWorking = useChatIsWorking(threadId)
  const [text, setText] = useState('')

  useEffect(() => {
    if (!threadId) return
    if (session.status !== 'joined') return
    let cancelled = false
    void (async () => {
      try {
        const page = await client.listEvents(threadId, { limit: 200 })
        if (cancelled) return
        for (const evt of page.items) {
          store.getState().actions.addEvent(evt)
        }
      } catch {}
    })()
    return () => {
      cancelled = true
    }
  }, [client, store, threadId, session.status])

  const submit = useCallback(() => {
    if (!threadId) return
    const trimmed = text.trim()
    if (!trimmed) return
    void client.sendMessage(threadId, {
      clientId: crypto.randomUUID(),
      content: [{ type: 'text', text: trimmed }],
    })
    setText('')
  }, [client, text, threadId])

  return { session, events, isWorking, text, setText, submit }
}
