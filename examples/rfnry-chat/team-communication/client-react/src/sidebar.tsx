import {
  type UserIdentity,
  useChatClient,
  useCreateThread,
  useQueryClient,
  useThreads,
} from '@rfnry/chat-client-react'
import { useCallback } from 'react'
import {
  findOrg,
  ORGANIZATIONS,
  type Organization,
  type OrgId,
  ROLES,
  type Role,
  type WorkspaceId,
} from './tenants'
import { buttonCls } from './ui'

function tryFindOrg(id: string): Organization | null {
  try {
    return findOrg(id as OrgId)
  } catch {
    return null
  }
}

type Props = {
  org: Organization
  workspaceId: WorkspaceId
  role: Role
  selectedThreadId: string | null
  onPickOrg: (id: OrgId) => void
  onPickWorkspace: (id: WorkspaceId) => void
  onPickRole: (id: Role) => void
  onPickThread: (id: string | null) => void
  identity: UserIdentity
  authorId: string
}

export function Sidebar({
  org,
  workspaceId,
  role,
  selectedThreadId,
  onPickOrg,
  onPickWorkspace,
  onPickRole,
  onPickThread,
  identity,
  authorId,
}: Props) {
  const client = useChatClient()
  const queryClient = useQueryClient()
  const { data, isLoading } = useThreads({ limit: 50 })
  const { mutateAsync: createThread, isPending } = useCreateThread()
  const threads = data?.items ?? []

  const handleNewThread = useCallback(async () => {
    const thread = await createThread({
      tenant: { organization: org.id, workspace: workspaceId, author: authorId },
      clientId: crypto.randomUUID(),
    })
    await client.addMember(thread.id, org.agent)
    onPickThread(thread.id)
  }, [authorId, client, createThread, onPickThread, org.agent, org.id, workspaceId])

  const handleClear = useCallback(
    (threadId: string) => {
      void client.clearThreadEvents(threadId)
    },
    [client]
  )

  const handleDelete = useCallback(
    async (threadId: string) => {
      await client.deleteThread(threadId)
      await queryClient.invalidateQueries({ queryKey: ['chat', 'threads'] })
      if (selectedThreadId === threadId) onPickThread(null)
    },
    [client, onPickThread, queryClient, selectedThreadId]
  )

  return (
    <aside className="flex flex-col gap-4 border border-neutral-800 p-3 text-xs">
      <section className="flex flex-col gap-2">
        <span className="text-neutral-500">organization</span>
        <div className="flex gap-1">
          {ORGANIZATIONS.map((o) => (
            <button
              key={o.id}
              type="button"
              onClick={() => onPickOrg(o.id)}
              className={`flex-1 px-2 py-1 border ${
                o.id === org.id
                  ? 'border-neutral-200 bg-neutral-200 text-black'
                  : 'border-neutral-700 text-neutral-300 hover:border-neutral-500'
              }`}
            >
              {o.label}
            </button>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-2">
        <span className="text-neutral-500">workspace</span>
        <div className="flex flex-col gap-1">
          {org.workspaces.map((w) => (
            <button
              key={w.id}
              type="button"
              onClick={() => onPickWorkspace(w.id)}
              className={`text-left px-2 py-1 border ${
                w.id === workspaceId
                  ? 'border-neutral-200 bg-neutral-200 text-black'
                  : 'border-neutral-700 text-neutral-300 hover:border-neutral-500'
              }`}
            >
              {w.label}
            </button>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-2">
        <span className="text-neutral-500">role</span>
        <div className="flex flex-col gap-1">
          {ROLES.map((r) => (
            <button
              key={r.id}
              type="button"
              onClick={() => onPickRole(r.id)}
              className={`text-left px-2 py-1 border ${
                r.id === role
                  ? 'border-neutral-200 bg-neutral-200 text-black'
                  : 'border-neutral-700 text-neutral-300 hover:border-neutral-500'
              }`}
            >
              <div>{r.label}</div>
              <div
                className={`text-[10px] ${r.id === role ? 'text-neutral-600' : 'text-neutral-500'}`}
              >
                {r.blurb}
              </div>
            </button>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-2 flex-1 min-h-0">
        <div className="flex items-center justify-between">
          <span className="text-neutral-500">threads</span>
          <button
            type="button"
            onClick={() => void handleNewThread()}
            disabled={isPending}
            className={buttonCls}
          >
            + new
          </button>
        </div>
        <ul className="flex flex-col gap-1 overflow-auto max-h-96">
          {isLoading && <li className="text-neutral-600 italic">loading…</li>}
          {!isLoading && threads.length === 0 && (
            <li className="text-neutral-600 italic">nothing visible at this scope</li>
          )}
          {threads.map((t) => {
            const threadAuthor = typeof t.tenant.author === 'string' ? t.tenant.author : '?'
            const threadOrgId =
              typeof t.tenant.organization === 'string' ? t.tenant.organization : null
            const threadOrg = threadOrgId ? tryFindOrg(threadOrgId) : null
            const isSelected = selectedThreadId === t.id
            return (
              <li
                key={t.id}
                className={`border ${
                  isSelected ? 'border-neutral-200' : 'border-neutral-800 hover:border-neutral-600'
                }`}
              >
                <button
                  type="button"
                  onClick={() => onPickThread(t.id)}
                  className={`w-full text-left px-2 py-1 ${
                    isSelected ? 'text-neutral-200' : 'text-neutral-400'
                  }`}
                >
                  <div className="truncate">{t.id}</div>
                  <div className="text-[10px] text-neutral-600">
                    by {threadAuthor} · {threadOrg ? threadOrg.agent.name : '?'} ·{' '}
                    {new Date(t.createdAt).toLocaleTimeString()}
                  </div>
                </button>
                <div className="flex gap-1 px-2 pb-1">
                  <button
                    type="button"
                    onClick={() => handleClear(t.id)}
                    className="text-[10px] text-neutral-500 hover:text-neutral-300"
                    title="clear thread history, keep thread"
                  >
                    clear
                  </button>
                  <button
                    type="button"
                    onClick={() => void handleDelete(t.id)}
                    className="text-[10px] text-neutral-500 hover:text-red-400"
                    title="delete thread entirely"
                  >
                    delete
                  </button>
                </div>
              </li>
            )
          })}
        </ul>
      </section>

      <section className="text-[10px] text-neutral-600 border-t border-neutral-900 pt-2">
        <div>
          identity tenant:{' '}
          <span className="text-neutral-400">{JSON.stringify(identity.metadata.tenant)}</span>
        </div>
      </section>
    </aside>
  )
}
