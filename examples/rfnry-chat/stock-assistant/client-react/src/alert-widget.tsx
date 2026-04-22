import { useCallback, useEffect, useState } from 'react'
import { buttonCls, inputCls } from './ui'

type Props = {
  webhookUrl: string
  defaultUserId: string
  selectedThreadId: string | null
}

type Mode = 'new-thread' | 'existing-thread'

export function AlertWidget({ webhookUrl, defaultUserId, selectedThreadId }: Props) {
  const [mode, setMode] = useState<Mode>('new-thread')
  const [userId, setUserId] = useState(defaultUserId)
  const [threadId, setThreadId] = useState(selectedThreadId ?? '')
  const [message, setMessage] = useState('AAPL just crossed 200 — want a read?')
  const [status, setStatus] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (mode === 'existing-thread' && selectedThreadId) setThreadId(selectedThreadId)
  }, [mode, selectedThreadId])

  const submit = useCallback(async () => {
    setBusy(true)
    setStatus(null)
    try {
      const body: Record<string, string> = {
        user_id: userId.trim(),
        message: message.trim(),
      }
      if (mode === 'existing-thread' && threadId.trim()) body.thread_id = threadId.trim()
      const res = await fetch(`${webhookUrl}/alert-user`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!res.ok) {
        const detail = await res.text()
        setStatus(`error: ${res.status} ${detail}`)
        return
      }
      const data = await res.json()
      setStatus(`ok — thread ${data.thread_id}`)
    } catch (err) {
      setStatus(`failed: ${(err as Error).message}`)
    } finally {
      setBusy(false)
    }
  }, [message, mode, threadId, userId, webhookUrl])

  return (
    <section className="border border-neutral-800 p-3 flex flex-col gap-2 text-xs">
      <div className="flex items-center justify-between">
        <div className="text-neutral-500">
          trigger /alert-user — make the agent open a thread with someone
        </div>
        <div className="flex gap-1">
          <button
            type="button"
            onClick={() => setMode('new-thread')}
            className={`px-2 py-1 border ${
              mode === 'new-thread'
                ? 'border-neutral-200 bg-neutral-200 text-black'
                : 'border-neutral-700 text-neutral-400'
            }`}
          >
            new thread
          </button>
          <button
            type="button"
            onClick={() => setMode('existing-thread')}
            className={`px-2 py-1 border ${
              mode === 'existing-thread'
                ? 'border-neutral-200 bg-neutral-200 text-black'
                : 'border-neutral-700 text-neutral-400'
            }`}
          >
            into existing thread
          </button>
        </div>
      </div>
      <div className="grid grid-cols-[140px_1fr] gap-2 items-center">
        <label htmlFor="alert-user-id" className="text-neutral-500">
          user_id
        </label>
        <input
          id="alert-user-id"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className={inputCls}
        />
        {mode === 'existing-thread' && (
          <>
            <label htmlFor="alert-thread-id" className="text-neutral-500">
              thread_id
            </label>
            <input
              id="alert-thread-id"
              value={threadId}
              onChange={(e) => setThreadId(e.target.value)}
              placeholder="th_…"
              className={inputCls}
            />
          </>
        )}
        <label htmlFor="alert-message" className="text-neutral-500">
          message
        </label>
        <input
          id="alert-message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className={inputCls}
        />
      </div>
      <div className="flex items-center justify-between">
        <span className="text-neutral-600 text-[10px]">
          {status ?? 'the agent will open a thread, invite user_id, and send the message.'}
        </span>
        <button type="button" onClick={() => void submit()} disabled={busy} className={buttonCls}>
          {busy ? 'sending…' : 'alert'}
        </button>
      </div>
    </section>
  )
}
