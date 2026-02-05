import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { sendMessage } from '../features/chat/chatSlice'

export default function ChatInterface() {
  const [message, setMessage] = useState('')
  const dispatch = useDispatch()
  const { messages, loading } = useSelector((state) => state.chat)

  const onSend = async (e) => {
    e.preventDefault()
    if (!message.trim()) return
    await dispatch(sendMessage(message))
    setMessage('')
  }

  return (
    <div className="card">
      <h2>Conversational AI Logging</h2>
      <p className="hint">Try: "Log interaction for Dr Shah: discussed trial outcomes and safety concerns."</p>
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`msg ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'Agent'}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <form onSubmit={onSend} className="inline-form">
        <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Ask agent or log by conversation" />
        <button type="submit" disabled={loading}>{loading ? 'Sending...' : 'Send'}</button>
      </form>
    </div>
  )
}
