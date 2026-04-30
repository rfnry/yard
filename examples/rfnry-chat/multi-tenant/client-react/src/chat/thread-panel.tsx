import { buttonCls, EventFeed, inputCls } from './ui'
import { usePageThreadPanel } from './use-page-thread-panel'

type Props = {
  threadId: string | null
}

export function ThreadPanel({ threadId }: Props) {
  const page = usePageThreadPanel(threadId)

  if (!threadId)
    return (
      <section className="border border-neutral-800 p-4 text-xs text-neutral-500">
        pick a thread on the left, or start a new one.
      </section>
    )
  if (page.session.status === 'joining')
    return <p className="text-neutral-500 text-xs p-4">joining…</p>
  if (page.session.status === 'error')
    return <p className="text-red-400 text-xs p-4">error: {page.session.error?.message}</p>

  return (
    <section className="flex flex-col gap-3 border border-neutral-800 p-3">
      <header className="text-[10px] text-neutral-500">
        thread <span className="text-neutral-300">{threadId}</span>
      </header>
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
          placeholder="Say something…"
          className={inputCls}
        />
        <button type="submit" className={buttonCls}>
          send
        </button>
      </form>
    </section>
  )
}
