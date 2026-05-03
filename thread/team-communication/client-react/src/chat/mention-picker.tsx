import type { Identity } from '@rfnry/chat-client-react'
import { useEffect, useState } from 'react'

type Props = {
  members: Identity[]
  query: string
  onSelect: (member: Identity) => void
  onClose: () => void
}

function matchesQuery(member: Identity, query: string): boolean {
  if (!query) return true
  const q = query.toLowerCase()
  return member.name.toLowerCase().includes(q) || member.id.toLowerCase().includes(q)
}

export function MentionPicker({ members, query, onSelect, onClose }: Props) {
  const filtered = members.filter((m) => matchesQuery(m, query))
  const [highlight, setHighlight] = useState(0)

  // biome-ignore lint/correctness/useExhaustiveDependencies: query change is the trigger; we intentionally do not read it inside.
  useEffect(() => {
    setHighlight(0)
  }, [query])

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        e.preventDefault()
        onClose()
      } else if (e.key === 'ArrowDown') {
        e.preventDefault()
        setHighlight((h) => (filtered.length === 0 ? 0 : (h + 1) % filtered.length))
      } else if (e.key === 'ArrowUp') {
        e.preventDefault()
        setHighlight((h) =>
          filtered.length === 0 ? 0 : (h - 1 + filtered.length) % filtered.length
        )
      } else if (e.key === 'Enter' || e.key === 'Tab') {
        if (filtered.length === 0) return
        e.preventDefault()
        const picked = filtered[highlight] ?? filtered[0]
        if (picked) onSelect(picked)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [filtered, highlight, onClose, onSelect])

  if (filtered.length === 0) {
    return <div className="border border-neutral-800 bg-neutral-950 text-neutral-500 text-xs p-2" />
  }

  return (
    <ul className="border border-neutral-800 bg-neutral-950 text-xs">
      {filtered.map((m, idx) => (
        <li key={m.id}>
          <button
            type="button"
            onMouseEnter={() => setHighlight(idx)}
            onClick={() => onSelect(m)}
            className={`w-full text-left px-3 py-1 ${
              idx === highlight ? 'bg-neutral-800 text-neutral-100' : 'text-neutral-300'
            }`}
          >
            <span className="font-medium">{m.name}</span>
            <span className="text-neutral-500 ml-2">@{m.id}</span>
          </button>
        </li>
      ))}
    </ul>
  )
}
