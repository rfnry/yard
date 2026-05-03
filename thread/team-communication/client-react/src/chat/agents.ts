export type AgentSpec = {
  id: string
  name: string
  webhookUrl: string
}

export const AGENTS: AgentSpec[] = [
  { id: 'agent-a', name: 'Agent A', webhookUrl: 'http://localhost:9100' },
  { id: 'agent-b', name: 'Agent B', webhookUrl: 'http://localhost:9101' },
  { id: 'agent-c', name: 'Agent C', webhookUrl: 'http://localhost:9102' },
]

export function webhookFor(agentId: string): string | null {
  return AGENTS.find((a) => a.id === agentId)?.webhookUrl ?? null
}
