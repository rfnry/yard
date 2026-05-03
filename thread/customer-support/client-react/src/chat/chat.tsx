import type { Identity, UserIdentity } from '@rfnry/chat-client-react'
import { buttonCls, EventFeed, inputCls } from './ui'
import { usePageChat } from './use-page-chat'

const AGENT: Identity = {
  role: 'assistant',
  id: 'cs-agent',
  name: 'Customer Support',
  metadata: {},
}

export function Chat({ identity }: { identity: UserIdentity }) {
  const page = usePageChat({ identity, agent: AGENT })

  if (!page.threadId) return <p className="text-neutral-500 text-xs">opening thread…</p>
  if (page.session.status === 'joining')
    return <p className="text-neutral-500 text-xs">joining…</p>
  if (page.session.status === 'error')
    return <p className="text-red-400 text-xs">error: {page.session.error?.message}</p>

  return (
    <section className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <span className="text-[10px] text-neutral-600">thread {page.threadId}</span>
        <button
          type="button"
          onClick={page.clearHistory}
          className="text-xs text-neutral-500 hover:text-neutral-300"
        >
          clear history
        </button>
      </div>
      <EventFeed events={page.events} />
      {page.isWorking && <div className="text-neutral-500 text-xs">assistant is working…</div>}
      <form
        onSubmit={(e) => {
          e.preventDefault()
          page.submit()
        }}
        className="flex gap-2"
      >
        <input
          value={page.text}
          onChange={(e) => page.setText(e.target.value)}
          placeholder="Say hi…"
          className={inputCls}
        />
        <button type="submit" className={buttonCls}>
          send
        </button>
      </form>
    </section>
  )
}
