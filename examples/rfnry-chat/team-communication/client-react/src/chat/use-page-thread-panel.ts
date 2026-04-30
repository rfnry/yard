import {
  type ChatSession,
  type Identity,
  type Thread,
  useChatClient,
  useChatIsWorking,
  useChatMembers,
  useChatSession,
  useChatThread,
} from '@rfnry/chat-client-react'
import { useCallback } from 'react'

export type PageThreadPanelViewModel = {
  session: ChatSession
  isWorking: boolean
  members: Identity[]
  thread: Thread | null
  submit: (trimmed: string) => void
}

export function usePageThreadPanel(threadId: string | null): PageThreadPanelViewModel {
  const client = useChatClient()
  const session = useChatSession(threadId)
  const isWorking = useChatIsWorking(threadId)
  const members = useChatMembers(threadId)
  const thread = useChatThread(threadId)

  const submit = useCallback(
    (trimmed: string) => {
      if (!threadId) return
      void client.sendMessage(threadId, {
        clientId: crypto.randomUUID(),
        content: [{ type: 'text', text: trimmed }],
      })
    },
    [client, threadId]
  )

  return { session, isWorking, members, thread, submit }
}
