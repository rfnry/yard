/** Stable `client_id` for a DM thread between two participants.
 *  The server dedups threads by (caller, client_id), so two participants
 *  creating a thread with the same formula land on the same thread. */
export function dmClientId(a: string, b: string): string {
  return `dm_${[a, b].sort().join('__')}`
}
