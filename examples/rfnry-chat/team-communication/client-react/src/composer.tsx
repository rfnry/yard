import type { Identity } from '@rfnry/chat-client-react'
import { useCallback, useState } from 'react'
import { MentionPicker } from './mention-picker'
import { buttonCls, inputCls } from './ui'

type Props = {
  members: Identity[]
  isChannel: boolean
  onSubmit: (text: string) => void
}

type PickerState = { at: number; query: string } | null

function detectPicker(text: string, cursor: number, isChannel: boolean): PickerState {
  if (!isChannel) return null
  let at = -1
  for (let i = cursor - 1; i >= 0; i--) {
    const ch = text[i]
    if (ch === '@') {
      at = i
      break
    }
    if (!ch || /\s/.test(ch)) break
  }
  if (at < 0) return null
  const query = text.slice(at + 1, cursor)
  if (/\s/.test(query)) return null
  return { at, query }
}

export function ComposerForm({ members, isChannel, onSubmit }: Props) {
  const [text, setText] = useState('')
  const [picker, setPicker] = useState<PickerState>(null)

  const onChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value
      const cursor = e.target.selectionStart ?? value.length
      setText(value)
      setPicker(detectPicker(value, cursor, isChannel))
    },
    [isChannel]
  )

  const onSelectMember = useCallback(
    (m: Identity) => {
      if (!picker) return
      const before = text.slice(0, picker.at)
      const after = text.slice(picker.at + 1 + picker.query.length)
      const next = `${before}@${m.id} ${after}`
      setText(next)
      setPicker(null)
    },
    [picker, text]
  )

  const submit = useCallback(() => {
    const trimmed = text.trim()
    if (!trimmed) return
    onSubmit(trimmed)
    setText('')
    setPicker(null)
  }, [text, onSubmit])

  return (
    <div className="relative">
      {picker !== null && (
        <div className="absolute bottom-full left-0 right-0 mb-1 z-10">
          <MentionPicker
            members={members}
            query={picker.query}
            onSelect={onSelectMember}
            onClose={() => setPicker(null)}
          />
        </div>
      )}
      <form
        onSubmit={(e) => {
          e.preventDefault()
          submit()
        }}
        className="flex gap-2"
      >
        <input value={text} onChange={onChange} placeholder="Say something…" className={inputCls} />
        <button type="submit" className={buttonCls}>
          send
        </button>
      </form>
    </div>
  )
}
