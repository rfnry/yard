import type { Identity } from '@rfnry/chat-client-react'
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { MentionPicker } from '../src/chat/mention-picker'

const members: Identity[] = [
  { id: 'engineer', role: 'assistant', name: 'Engineer', metadata: {} },
  { id: 'coordinator', role: 'assistant', name: 'Coordinator', metadata: {} },
  { id: 'liaison', role: 'assistant', name: 'Liaison', metadata: {} },
]

describe('MentionPicker', () => {
  it('lists all eligible members when query is empty', () => {
    render(<MentionPicker members={members} query="" onSelect={vi.fn()} onClose={vi.fn()} />)
    expect(screen.getByText('Engineer')).toBeInTheDocument()
    expect(screen.getByText('Coordinator')).toBeInTheDocument()
    expect(screen.getByText('Liaison')).toBeInTheDocument()
  })

  it('filters by display name substring case-insensitively', () => {
    render(<MentionPicker members={members} query="eng" onSelect={vi.fn()} onClose={vi.fn()} />)
    expect(screen.getByText('Engineer')).toBeInTheDocument()
    expect(screen.queryByText('Coordinator')).toBeNull()
  })

  it('also filters by id substring', () => {
    render(
      <MentionPicker members={members} query="liaison" onSelect={vi.fn()} onClose={vi.fn()} />,
    )
    expect(screen.getByText('Liaison')).toBeInTheDocument()
    expect(screen.queryByText('Engineer')).toBeNull()
  })

  it('calls onSelect with first member on Enter when query is empty', () => {
    const onSelect = vi.fn()
    render(<MentionPicker members={members} query="" onSelect={onSelect} onClose={vi.fn()} />)
    fireEvent.keyDown(window, { key: 'Enter' })
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'engineer' }))
  })

  it('calls onClose on Escape', () => {
    const onClose = vi.fn()
    render(<MentionPicker members={members} query="" onSelect={vi.fn()} onClose={onClose} />)
    fireEvent.keyDown(window, { key: 'Escape' })
    expect(onClose).toHaveBeenCalled()
  })

  it('ArrowDown advances highlight', () => {
    const onSelect = vi.fn()
    render(<MentionPicker members={members} query="" onSelect={onSelect} onClose={vi.fn()} />)
    fireEvent.keyDown(window, { key: 'ArrowDown' })
    fireEvent.keyDown(window, { key: 'Enter' })
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'coordinator' }))
  })

  it('ArrowUp wraps to last when at first', () => {
    const onSelect = vi.fn()
    render(<MentionPicker members={members} query="" onSelect={onSelect} onClose={vi.fn()} />)
    fireEvent.keyDown(window, { key: 'ArrowUp' })
    fireEvent.keyDown(window, { key: 'Enter' })
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'liaison' }))
  })

  it('clicking an item selects it', () => {
    const onSelect = vi.fn()
    render(<MentionPicker members={members} query="" onSelect={onSelect} onClose={vi.fn()} />)
    fireEvent.click(screen.getByText('Coordinator'))
    expect(onSelect).toHaveBeenCalledWith(expect.objectContaining({ id: 'coordinator' }))
  })

  it('renders empty list when query matches nothing', () => {
    render(<MentionPicker members={members} query="zzz" onSelect={vi.fn()} onClose={vi.fn()} />)
    expect(screen.queryByText('Engineer')).toBeNull()
    expect(screen.queryByText('Coordinator')).toBeNull()
    expect(screen.queryByText('Liaison')).toBeNull()
  })
})
