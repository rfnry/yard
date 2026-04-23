import type { Identity, Thread } from '@rfnry/chat-client-react'

/** Stable `client_id` for a DM thread between two participants.
 *  The server dedups threads by (caller, client_id), so two participants
 *  creating a thread with the same formula land on the same thread.
 *  Kept for reference; the example now uses `POST /chat/dm` for find-or-create
 *  because per-caller dedup broke cross-caller lookups (agent vs user). */
export function dmClientId(a: string, b: string): string {
  return `dm_${[a, b].sort().join('__')}`
}

/** Base64url-encode the identity the same way `@rfnry/chat-client-react` does
 *  for its socket/REST auth. The server example uses `resolve_identity`, which
 *  reads `x-rfnry-identity`, so we need the same encoding here. */
function encodeIdentity(identity: Identity): string {
  return btoa(JSON.stringify(identity)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
}

/** Find-or-create the DM thread between `self` and `other`.
 *
 *  Calls the example server's `POST /chat/dm` endpoint which dedups by member
 *  set (cross-caller) rather than by `(caller, client_id)`. For self-DMs
 *  (`self.id === other.id`), `with_identity` is ignored. */
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
