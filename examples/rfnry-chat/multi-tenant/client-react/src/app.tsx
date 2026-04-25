import { ChatProvider, type UserIdentity } from '@rfnry/chat-client-react'
import { useMemo, useState } from 'react'
import { Sidebar } from './sidebar'
import {
  findOrg,
  ORGANIZATIONS,
  type OrgId,
  type Role,
  tenantFor,
  type WorkspaceId,
} from './tenants'
import { ThreadPanel } from './thread-panel'

const SERVER_URL = import.meta.env.VITE_CHAT_SERVER_URL ?? 'http://localhost:8000'

const GUEST_KEY = 'rfnry-multi-tenant-guest'

function loadOrMakeGuest(): { id: string; name: string } {
  try {
    const raw = sessionStorage.getItem(GUEST_KEY)
    if (raw) {
      const parsed = JSON.parse(raw) as { id: string; name: string }
      if (parsed?.id && parsed?.name) return parsed
    }
  } catch {}
  const suffix = Math.floor(1000 + Math.random() * 9000)
  const guest = {
    id: `u_${crypto.randomUUID().slice(0, 8)}`,
    name: `Guest-${suffix}`,
  }
  try {
    sessionStorage.setItem(GUEST_KEY, JSON.stringify(guest))
  } catch {}
  return guest
}

export function App() {
  const guest = useMemo(loadOrMakeGuest, [])
  const [orgId, setOrgId] = useState<OrgId>(ORGANIZATIONS[0]!.id)
  const [workspaceId, setWorkspaceId] = useState<WorkspaceId>(ORGANIZATIONS[0]!.workspaces[0]!.id)
  const [role, setRole] = useState<Role>('member')
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null)

  const org = findOrg(orgId)
  const workspace = org.workspaces.find((w) => w.id === workspaceId) ?? org.workspaces[0]!
  const effectiveWorkspaceId = workspace.id

  const identity: UserIdentity = useMemo(
    () => ({
      role: 'user',
      id: guest.id,
      name: guest.name,
      metadata: {
        tenant: tenantFor(role, org.id, effectiveWorkspaceId, guest.id),
      },
    }),
    [guest.id, guest.name, org.id, effectiveWorkspaceId, role]
  )

  const handlePickOrg = (next: OrgId) => {
    setOrgId(next)
    const nextOrg = findOrg(next)
    setWorkspaceId(nextOrg.workspaces[0]!.id)
    setSelectedThreadId(null)
  }

  const handlePickWorkspace = (next: WorkspaceId) => {
    setWorkspaceId(next)
    setSelectedThreadId(null)
  }

  const handlePickRole = (next: Role) => {
    setRole(next)
    setSelectedThreadId(null)
  }

  return (
    <div className="min-h-screen max-w-5xl mx-auto px-6 py-6 font-mono">
      <header className="mb-4 flex items-center justify-between flex-wrap gap-2">
        <h1 className="text-xl">multi-tenant</h1>
        <p className="text-xs text-neutral-500">
          you are <span className="text-neutral-200">{guest.name}</span>{' '}
          <span className="text-neutral-600">({guest.id})</span>
        </p>
      </header>

      <ChatProvider
        key={guest.id}
        url={SERVER_URL}
        identity={identity}
        fallback={<p className="text-neutral-500 text-xs">Connecting…</p>}
        errorFallback={
          <p className="text-red-400 text-xs">
            Unable to reach the multi-tenant chat server at {SERVER_URL}.
          </p>
        }
      >
        <div className="grid grid-cols-[280px_1fr] gap-4">
          <Sidebar
            org={org}
            workspaceId={effectiveWorkspaceId}
            role={role}
            selectedThreadId={selectedThreadId}
            onPickOrg={handlePickOrg}
            onPickWorkspace={handlePickWorkspace}
            onPickRole={handlePickRole}
            onPickThread={setSelectedThreadId}
            identity={identity}
            authorId={guest.id}
          />
          <ThreadPanel key={selectedThreadId ?? 'none'} threadId={selectedThreadId} />
        </div>
      </ChatProvider>
    </div>
  )
}
