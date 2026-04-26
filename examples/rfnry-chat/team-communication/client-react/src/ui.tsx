import type { Event } from '@rfnry/chat-client-react'
import { type Identity, parseMemberMentions, useThreadFeed } from '@rfnry/chat-client-react'
import type React from 'react'

type EventFeedProps = {
  threadId: string | null
  members: Identity[]
  showRunEvents?: boolean
}

export function EventFeed({ threadId, members, showRunEvents = true }: EventFeedProps) {
  const feed = useThreadFeed(threadId)
  const filtered = showRunEvents
    ? feed
    : feed.filter((item) => {
        if (item.kind === 'streaming') return true
        return item.event.type !== 'run.started' && item.event.type !== 'run.completed'
      })
  return (
    <ul className="flex flex-col gap-1 border border-neutral-800 bg-neutral-950 p-3 max-h-96 overflow-auto text-xs">
      {filtered.length === 0 && (
        <li className="text-neutral-600 italic">no events yet — send one below</li>
      )}
      {filtered.map((item) => {
        if (item.kind === 'event') {
          return (
            <li
              key={item.event.id}
              className="text-neutral-300 border-b border-neutral-900 last:border-0 py-1"
            >
              <EventBubble event={item.event} members={members} />
            </li>
          )
        }
        return (
          <li
            key={item.eventId}
            className="text-neutral-300 border-b border-neutral-900 last:border-0 py-1"
          >
            <StreamingBubble author={item.author} text={item.text} members={members} />
          </li>
        )
      })}
    </ul>
  )
}

function renderTextWithMentions(text: string, members: Identity[]): React.ReactNode[] {
  const { spans } = parseMemberMentions(text, members)
  if (!spans.length) return [text]
  const byId = new Map(members.map((m) => [m.id, m]))
  const parts: React.ReactNode[] = []
  let cursor = 0
  for (const span of spans) {
    if (span.start > cursor) parts.push(text.slice(cursor, span.start))
    const display = byId.get(span.identityId)?.name ?? span.identityId
    parts.push(
      <span
        key={`${span.start}-${span.identityId}`}
        className="text-blue-400 bg-blue-500/10 px-1 rounded"
      >
        @{display}
      </span>
    )
    cursor = span.start + span.length
  }
  if (cursor < text.length) parts.push(text.slice(cursor))
  return parts
}

type EventBubbleProps = {
  event: Event
  members: Identity[]
}

function EventBubble({ event: e, members }: EventBubbleProps): React.ReactNode {
  switch (e.type) {
    case 'message': {
      const text = e.content.find((p) => p.type === 'text')
      const body = text && text.type === 'text' ? text.text : '[media]'
      return (
        <>
          {e.author.name}: {renderTextWithMentions(body, members)}
        </>
      )
    }
    case 'reasoning':
      return `${e.author.name} (reasoning): ${e.content}`
    case 'tool.call':
      return `${e.author.name} → ${e.tool.name}(${JSON.stringify(e.tool.arguments)})`
    case 'tool.result':
      return `← ${e.tool.id}: ${
        e.tool.error ? `error ${e.tool.error.code}` : JSON.stringify(e.tool.result)
      }`
    case 'run.started':
      return '— run started —'
    case 'run.completed':
      return '— run completed —'
    case 'run.failed':
      return `— run failed: ${e.error.message} —`
    case 'run.cancelled':
      return '— run cancelled —'
    case 'thread.member_added':
      return `+ ${e.member.name} joined`
    case 'thread.member_removed':
      return `- ${e.member.name} left`
    default:
      return `[${e.type}]`
  }
}

type StreamingBubbleProps = {
  author: Identity
  text: string
  members: Identity[]
}

function StreamingBubble({ author, text, members }: StreamingBubbleProps): React.ReactNode {
  return (
    <span className="border-l-2 border-blue-500/30 pl-2">
      {author.name}:{' '}
      <span className="opacity-80">
        {renderTextWithMentions(text, members)}
        <span className="animate-pulse">▍</span>
      </span>
    </span>
  )
}

export const inputCls =
  'flex-1 bg-neutral-950 border border-neutral-800 px-3 py-2 text-sm focus:outline-none focus:border-neutral-500'
export const buttonCls =
  'bg-neutral-200 text-black px-3 py-2 text-sm hover:bg-neutral-300 active:bg-neutral-400 disabled:opacity-40'
