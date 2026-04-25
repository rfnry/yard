import { type UserIdentity, usePresence, useThreads } from '@rfnry/chat-client-react'
import { useEffect, useState } from 'react'
import { webhookFor } from './agents'
import { buttonCls } from './ui'

type Props = {
  identity: UserIdentity
}

export function PingControl({ identity }: Props) {
  const presence = usePresence()
  const { data: threadPage } = useThreads({ limit: 50 })
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

  const pingChannel = async () => {
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
  }

  const pingDirect = async () => {
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
  }

  return (
    <section className="mt-4 border-t border-neutral-800 pt-3 p-3 flex flex-col gap-2 text-xs">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-neutral-500">agent</span>
        <select
          value={agentId}
          onChange={(e) => setAgentId(e.target.value)}
          className="bg-neutral-900 border border-neutral-700 text-neutral-200 px-2 py-1"
        >
          {onlineAgents.length === 0 && <option value="">no agents online</option>}
          {onlineAgents.map((a) => (
            <option key={a.id} value={a.id}>
              {a.name}
            </option>
          ))}
        </select>

        <span className="text-neutral-500">channel</span>
        <select
          value={channelId}
          onChange={(e) => setChannelId(e.target.value)}
          className="bg-neutral-900 border border-neutral-700 text-neutral-200 px-2 py-1"
        >
          {channels.length === 0 && <option value="">no channels</option>}
          {channels.map((c) => {
            const label = (c.metadata as { label?: string } | undefined)?.label ?? c.id
            return (
              <option key={c.id} value={c.id}>
                # {label}
              </option>
            )
          })}
        </select>

        <button
          type="button"
          onClick={() => void pingChannel()}
          disabled={!agentId || !channelId || busy !== null}
          className={buttonCls}
        >
          {busy === 'channel' ? 'pinging…' : 'Ping in channel'}
        </button>

        <button
          type="button"
          onClick={() => void pingDirect()}
          disabled={!agentId || busy !== null}
          className={buttonCls}
        >
          {busy === 'direct' ? 'pinging…' : 'Ping me direct'}
        </button>
      </div>
      {status && <p className="text-neutral-500 text-[10px]">{status}</p>}
    </section>
  )
}
