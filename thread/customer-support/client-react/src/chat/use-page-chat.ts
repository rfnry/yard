import {
  type ChatSession,
  type Event,
  type Identity,
  useChatClient,
  useChatHistory,
  useChatIsWorking,
  useChatSession,
  type UserIdentity,
} from '@rfnry/chat-client-react'
import { useCallback, useState } from 'react'
import { useFreshThread } from './use-fresh-thread'

export type PageChatViewModel = {
  threadId: string | null
  session: ChatSession
  events: Event[]
  isWorking: boolean
  text: string
  setText: (next: string) => void
  submit: () => void
  clearHistory: () => void
}

export function usePageChat({
  identity,
  agent,
}: {
  identity: UserIdentity
  agent: Identity
}): PageChatViewModel {
  const threadId = useFreshThread(identity, agent)
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
      recipients: [agent.id],
    })
    setText('')
  }, [agent.id, client, text, threadId])

  const clearHistory = useCallback(() => {
    if (!threadId) return
    void client.clearThreadEvents(threadId)
  }, [client, threadId])

  return {
    threadId,
    session,
    events,
    isWorking,
    text,
    setText,
    submit,
    clearHistory,
  }
}
