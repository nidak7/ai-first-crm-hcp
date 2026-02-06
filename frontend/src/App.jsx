import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import InteractionList from './components/InteractionList'
import LogInteractionForm from './components/LogInteractionForm'

export default function App() {
  const [mode, setMode] = useState('form')

  return (
    <main className="container">
      <header>
        <h1>AI-First CRM | HCP Log Interaction Screen</h1>
        <div className="tab-row">
          <button className={mode === 'form' ? 'active' : ''} onClick={() => setMode('form')}>Structured Form</button>
          <button className={mode === 'chat' ? 'active' : ''} onClick={() => setMode('chat')}>Conversational Chat</button>
        </div>
      </header>
      {mode === 'form' ? <LogInteractionForm /> : <ChatInterface />}
      <InteractionList />
    </main>
  )
}
