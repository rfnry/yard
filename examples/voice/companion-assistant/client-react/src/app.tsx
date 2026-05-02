import { VoiceProvider } from '@rfnry/voice-client-react'
import { useState } from 'react'
import { Onboarding } from './onboarding'
import { Session } from './session'

const SERVER_URL =
  (import.meta.env.VITE_VOICE_SERVER_URL as string | undefined) ?? 'http://localhost:8401'

type Profile = { user: string; companion: string }

export function App() {
  const [profile, setProfile] = useState<Profile | null>(null)

  if (profile === null) {
    return <Onboarding onSubmit={setProfile} />
  }

  const offerUrl = `${SERVER_URL.replace(/\/$/, '')}/webrtc/offer/${encodeURIComponent(profile.user)}`

  return (
    <VoiceProvider serverUrl={offerUrl} transport="webrtc">
      <Session companion={profile.companion} />
    </VoiceProvider>
  )
}
