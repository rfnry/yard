import type { UserIdentity } from '@rfnry/chat-client-react'
import { buttonCls } from './ui'
import { usePagePingControl } from './use-page-ping-control'

type Props = {
  identity: UserIdentity
}

export function PingControl({ identity }: Props) {
  const page = usePagePingControl(identity)

  return (
    <section className="mt-4 border-t border-neutral-800 pt-3 p-3 flex flex-col gap-2 text-xs">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-neutral-500">agent</span>
        <select
          value={page.agentId}
          onChange={(e) => page.setAgentId(e.target.value)}
          className="bg-neutral-900 border border-neutral-700 text-neutral-200 px-2 py-1"
        >
          {page.onlineAgents.length === 0 && <option value="">no agents online</option>}
          {page.onlineAgents.map((a) => (
            <option key={a.id} value={a.id}>
              {a.name}
            </option>
          ))}
        </select>

        <span className="text-neutral-500">channel</span>
        <select
          value={page.channelId}
          onChange={(e) => page.setChannelId(e.target.value)}
          className="bg-neutral-900 border border-neutral-700 text-neutral-200 px-2 py-1"
        >
          {page.channels.length === 0 && <option value="">no channels</option>}
          {page.channels.map((c) => {
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
          onClick={() => void page.pingChannel()}
          disabled={!page.agentId || !page.channelId || page.busy !== null}
          className={buttonCls}
        >
          {page.busy === 'channel' ? 'pinging…' : 'Ping in channel'}
        </button>

        <button
          type="button"
          onClick={() => void page.pingDirect()}
          disabled={!page.agentId || page.busy !== null}
          className={buttonCls}
        >
          {page.busy === 'direct' ? 'pinging…' : 'Ping me direct'}
        </button>
      </div>
      {page.status && <p className="text-neutral-500 text-[10px]">{page.status}</p>}
    </section>
  )
}
