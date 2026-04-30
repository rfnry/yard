import {
  type AssistantIdentity,
  type Thread,
  useChatPresence,
  useChatThreads,
  type UserIdentity,
} from '@rfnry/chat-client-react'
import { useCallback, useEffect, useState } from 'react'
import { webhookFor } from './agents'

export type PagePingControlViewModel = {
  onlineAgents: AssistantIdentity[]
  channels: Thread[]
  agentId: string
  setAgentId: (id: string) => void
  channelId: string
  setChannelId: (id: string) => void
  busy: null | 'channel' | 'direct'
  status: string | null
  pingChannel: () => Promise<void>
  pingDirect: () => Promise<void>
}

export function usePagePingControl(identity: UserIdentity): PagePingControlViewModel {
  const presence = useChatPresence()
  const { data: threadPage } = useChatThreads({ limit: 50 })
  const channels =
    threadPage?.items.filter(
      (t) => (t.metadata as { kind?: string } | undefined)?.kind === 'channel'
    ) ?? []

  const onlineAgents = presence.byRole.assistant
  const [agentId, setAgentId] = useState('')
  const [channelId, setChannelId] = useState('')
  const [busy, setBusy] = useState<null | 'channel' | 'direct'>(null)
  const [status, setStatus] = useState<string | null>(null)

  useEffect(() => {
    if (!agentId && onlineAgents.length > 0) setAgentId(onlineAgents[0]!.id)
    if (agentId && !onlineAgents.some((a) => a.id === agentId)) {
      setAgentId(onlineAgents[0]?.id ?? '')
    }
  }, [agentId, onlineAgents])

  useEffect(() => {
    if (!channelId && channels.length > 0) setChannelId(channels[0]!.id)
  }, [channelId, channels])

  const pingChannel = useCallback(async () => {
    const url = webhookFor(agentId)
    if (!url || !channelId) return
    setBusy('channel')
    setStatus(null)
    try {
      const res = await fetch(`${url}/ping-channel`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          channel_id: channelId,
          requested_by: { id: identity.id, name: identity.name },
        }),
      })
      if (!res.ok) {
        setStatus(`error: ${res.status} ${await res.text()}`)
        return
      }
      const data = await res.json()
      setStatus(`ok — subject: ${data.subject ?? '(none)'}`)
    } catch (err) {
      setStatus(`failed: ${(err as Error).message}`)
    } finally {
      setBusy(null)
    }
  }, [agentId, channelId, identity.id, identity.name])

  const pingDirect = useCallback(async () => {
    const url = webhookFor(agentId)
    if (!url) return
    setBusy('direct')
    setStatus(null)
    try {
      const res = await fetch(`${url}/ping-direct`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          user_id: identity.id,
          user_name: identity.name,
          requested_by: { id: identity.id, name: identity.name },
        }),
      })
      if (!res.ok) {
        setStatus(`error: ${res.status} ${await res.text()}`)
        return
      }
      const data = await res.json()
      setStatus(`ok — DM thread: ${data.thread_id ?? '(none)'}`)
    } catch (err) {
      setStatus(`failed: ${(err as Error).message}`)
    } finally {
      setBusy(null)
    }
  }, [agentId, identity.id, identity.name])

  return {
    onlineAgents,
    channels,
    agentId,
    setAgentId,
    channelId,
    setChannelId,
    busy,
    status,
    pingChannel,
    pingDirect,
  }
}
