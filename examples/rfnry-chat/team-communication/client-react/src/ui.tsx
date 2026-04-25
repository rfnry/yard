import type { Event } from '@rfnry/chat-client-react'
import type React from 'react'

type EventFeedProps = {
  events: Event[]

  showRunEvents?: boolean
}

export function EventFeed({ events, showRunEvents = true }: EventFeedProps) {
  const filtered = showRunEvents
    ? events
    : events.filter((e) => e.type !== 'run.started' && e.type !== 'run.completed')
  return (
    <ul className="flex flex-col gap-1 border border-neutral-800 bg-neutral-950 p-3 max-h-96 overflow-auto text-xs">
      {filtered.length === 0 && (
        <li className="text-neutral-600 italic">no events yet — send one below</li>
      )}
      {filtered.map((e) => (
        <li key={e.id} className="text-neutral-300 border-b border-neutral-900 last:border-0 py-1">
          {renderEventNode(e)}
        </li>
      ))}
    </ul>
  )
}

function highlightMentions(text: string): React.ReactNode {
  const parts = text.split(/(@[\w-]+)/g)
  if (parts.length === 1) return text
  return parts.map((part, i) =>
    part.startsWith('@') ? (
      // biome-ignore lint/suspicious/noArrayIndexKey: static split of a string — order never changes
      <span key={i} className="text-blue-400">
        {part}
      </span>
    ) : (
      part
    )
  )
}

function renderEventNode(e: Event): React.ReactNode {
  switch (e.type) {
    case 'message': {
      const text = e.content.find((p) => p.type === 'text')
      const body = text && text.type === 'text' ? text.text : '[media]'
      return (
        <>
          {e.author.name}: {highlightMentions(body)}
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

export const inputCls =
  'flex-1 bg-neutral-950 border border-neutral-800 px-3 py-2 text-sm focus:outline-none focus:border-neutral-500'
export const buttonCls =
  'bg-neutral-200 text-black px-3 py-2 text-sm hover:bg-neutral-300 active:bg-neutral-400 disabled:opacity-40'
