import { FrequencyVisualizer, useVoiceSession } from '@rfnry/voice-client-react'

type SessionProps = {
  companion: string
}

export function Session({ companion }: SessionProps) {
  const { connect, disconnect, status, mute, isMuted } = useVoiceSession()

  return (
    <main className="session">
      <header>
        talking to <strong>{companion}</strong>
      </header>
      <FrequencyVisualizer
        mode="circular"
        userColor="#ffd97a"
        agentColor="#7aa9ff"
        width={360}
        height={360}
      />
      <footer>
        {status === 'idle' || status === 'error' ? (
          <button type="button" className="primary" onClick={connect}>
            talk to {companion}
          </button>
        ) : (
          <button type="button" onClick={disconnect}>
            end
          </button>
        )}
        <button type="button" onClick={mute}>
          {isMuted ? 'unmute' : 'mute'}
        </button>
        <span className="status">{status}</span>
      </footer>
    </main>
  )
}
