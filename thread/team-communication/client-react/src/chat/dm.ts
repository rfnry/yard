import type { Identity, Thread } from '@rfnry/chat-client-react'

export function dmClientId(a: string, b: string): string {
  return `dm_${[a, b].sort().join('__')}`
}

function encodeIdentity(identity: Identity): string {
  return btoa(JSON.stringify(identity)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
}

export async function findOrCreateDm(
  serverUrl: string,
  self: Identity,
  other: Identity
): Promise<Thread> {
  const res = await fetch(`${serverUrl.replace(/\/$/, '')}/chat/dm`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-rfnry-identity': encodeIdentity(self),
    },
    body: JSON.stringify({ with: other.id, with_identity: other }),
  })
  if (!res.ok) {
    throw new Error(`POST /chat/dm failed: ${res.status} ${await res.text()}`)
  }
  return (await res.json()) as Thread
}
