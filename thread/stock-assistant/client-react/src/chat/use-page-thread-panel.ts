import {
  type ChatSession,
  type Event,
  useChatClient,
  useChatHistory,
  useChatIsWorking,
  useChatSession,
} from '@rfnry/chat-client-react'
import { useCallback, useState } from 'react'

export type PageThreadPanelViewModel = {
  session: ChatSession
  events: Event[]
  isWorking: boolean
  text: string
  setText: (next: string) => void
  submit: () => void
}

export function usePageThreadPanel({
  threadId,
  agentId,
}: {
  threadId: string | null
  agentId: string
}): PageThreadPanelViewModel {
  const client = useChatClient()
  const session = useChatSession(threadId)
  const events = useChatHistory(threadId)
  const isWorking = useChatIsWorking(threadId)
  const [text, setText] = useState('')

  const submit = useCallback(() => {
    if (!threadId) return
    const trimmed = text.trim()
    if (!trimmed) return
    void client.sendMessage(threadId, {
      clientId: crypto.randomUUID(),
      content: [{ type: 'text', text: trimmed }],
      recipients: [agentId],
    })
    setText('')
  }, [agentId, client, text, threadId])

  return { session, events, isWorking, text, setText, submit }
}
