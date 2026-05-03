import type { AssistantIdentity } from '@rfnry/chat-client-react'

export type OrgId = 'organization-a' | 'organization-b'
export type WorkspaceId = 'workspace-a-1' | 'workspace-a-2' | 'workspace-b-1' | 'workspace-b-2'

export type Workspace = {
  id: WorkspaceId
  label: string
}

export type Organization = {
  id: OrgId
  label: string
  workspaces: Workspace[]
  agent: AssistantIdentity
}

export const ORGANIZATIONS: Organization[] = [
  {
    id: 'organization-a',
    label: 'Organization A',
    workspaces: [
      { id: 'workspace-a-1', label: 'Workspace A-1' },
      { id: 'workspace-a-2', label: 'Workspace A-2' },
    ],
    agent: {
      role: 'assistant',
      id: 'agent-a',
      name: 'Agent A',
      metadata: {
        tenant: { organization: 'organization-a', workspace: '*', author: '*' },
      },
    },
  },
  {
    id: 'organization-b',
    label: 'Organization B',
    workspaces: [
      { id: 'workspace-b-1', label: 'Workspace B-1' },
      { id: 'workspace-b-2', label: 'Workspace B-2' },
    ],
    agent: {
      role: 'assistant',
      id: 'agent-b',
      name: 'Agent B',
      metadata: {
        tenant: { organization: 'organization-b', workspace: '*', author: '*' },
      },
    },
  },
]

export function findOrg(id: OrgId): Organization {
  const org = ORGANIZATIONS.find((o) => o.id === id)
  if (!org) throw new Error(`unknown org ${id}`)
  return org
}

export type Role = 'system-admin' | 'org-manager' | 'workspace-manager' | 'member'

export const ROLES: { id: Role; label: string; blurb: string }[] = [
  {
    id: 'member',
    label: 'member',
    blurb: 'only own threads in current workspace',
  },
  {
    id: 'workspace-manager',
    label: 'workspace manager',
    blurb: 'every author, current workspace',
  },
  {
    id: 'org-manager',
    label: 'org manager',
    blurb: 'every workspace in the current org',
  },
  {
    id: 'system-admin',
    label: 'system admin',
    blurb: 'everything, every org',
  },
]

export function tenantFor(role: Role, orgId: OrgId, workspaceId: WorkspaceId, authorId: string) {
  switch (role) {
    case 'system-admin':
      return { organization: '*', workspace: '*', author: '*' }
    case 'org-manager':
      return { organization: orgId, workspace: '*', author: '*' }
    case 'workspace-manager':
      return { organization: orgId, workspace: workspaceId, author: '*' }
    case 'member':
      return { organization: orgId, workspace: workspaceId, author: authorId }
  }
}
