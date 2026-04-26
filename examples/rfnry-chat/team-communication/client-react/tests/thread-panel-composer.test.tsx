import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ComposerForm } from '../src/composer'

const channelMembers = [
  { id: 'engineer', role: 'assistant' as const, name: 'Engineer', metadata: {} },
  { id: 'coordinator', role: 'assistant' as const, name: 'Coordinator', metadata: {} },
  { id: 'liaison', role: 'assistant' as const, name: 'Liaison', metadata: {} },
]

describe('ComposerForm composer + picker integration', () => {
  it('typing "@" opens the picker', () => {
    render(<ComposerForm members={channelMembers} isChannel={true} onSubmit={vi.fn()} />)
    const input = screen.getByPlaceholderText('Say something…') as HTMLInputElement
    fireEvent.change(input, { target: { value: '@' } })
    expect(screen.getByText('Engineer')).toBeInTheDocument()
  })

  it('selecting a member inserts @<id> + space into the textarea', () => {
    render(<ComposerForm members={channelMembers} isChannel={true} onSubmit={vi.fn()} />)
    const input = screen.getByPlaceholderText('Say something…') as HTMLInputElement
    fireEvent.change(input, { target: { value: '@en' } })
    fireEvent.click(screen.getByText('Engineer'))
    expect(input.value).toBe('@engineer ')
  })

  it('submitting sends prose with NO recipients (server parses)', () => {
    const onSubmit = vi.fn()
    render(<ComposerForm members={channelMembers} isChannel={true} onSubmit={onSubmit} />)
    const input = screen.getByPlaceholderText('Say something…') as HTMLInputElement
    fireEvent.change(input, { target: { value: 'hi @engineer' } })
    fireEvent.submit(input.closest('form')!)
    expect(onSubmit).toHaveBeenCalledWith('hi @engineer')
  })

  it('Escape closes the picker', () => {
    render(<ComposerForm members={channelMembers} isChannel={true} onSubmit={vi.fn()} />)
    const input = screen.getByPlaceholderText('Say something…') as HTMLInputElement
    fireEvent.change(input, { target: { value: '@' } })
    expect(screen.getByText('Engineer')).toBeInTheDocument()
    fireEvent.keyDown(window, { key: 'Escape' })
    expect(screen.queryByText('Engineer')).toBeNull()
  })

  it('typing whitespace after @<query> closes the picker', () => {
    render(<ComposerForm members={channelMembers} isChannel={true} onSubmit={vi.fn()} />)
    const input = screen.getByPlaceholderText('Say something…') as HTMLInputElement
    fireEvent.change(input, { target: { value: '@en' } })
    expect(screen.getByText('Engineer')).toBeInTheDocument()
    fireEvent.change(input, { target: { value: '@en ' } })
    expect(screen.queryByText('Engineer')).toBeNull()
  })

  it('does not show picker outside channels (still works as plain composer)', () => {
    render(<ComposerForm members={channelMembers} isChannel={false} onSubmit={vi.fn()} />)
    const input = screen.getByPlaceholderText('Say something…') as HTMLInputElement
    fireEvent.change(input, { target: { value: '@' } })
    expect(screen.queryByText('Engineer')).toBeNull()
  })
})
