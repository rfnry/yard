import { useState } from 'react'

type OnboardingProps = {
  onSubmit: (profile: { user: string; companion: string }) => void
}

export function Onboarding({ onSubmit }: OnboardingProps) {
  const [user, setUser] = useState('')
  const [companion, setCompanion] = useState('Sam')

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    const trimmedUser = user.trim()
    const trimmedCompanion = companion.trim() || 'Sam'
    if (!trimmedUser.match(/^[A-Za-z0-9_-]+$/)) {
      alert('your name must be alphanumeric (dashes/underscores ok)')
      return
    }
    onSubmit({ user: trimmedUser, companion: trimmedCompanion })
  }

  return (
    <main className="onboarding">
      <form onSubmit={submit}>
        <h1>companion-assistant</h1>
        <label>
          your name
          <input
            type="text"
            value={user}
            onChange={(e) => setUser(e.target.value)}
            placeholder="alice"
          />
        </label>
        <label>
          companion's name
          <input
            type="text"
            value={companion}
            onChange={(e) => setCompanion(e.target.value)}
            placeholder="Sam"
          />
        </label>
        <button type="submit" className="primary">
          start
        </button>
      </form>
    </main>
  )
}
