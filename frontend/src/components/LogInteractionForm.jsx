import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { createInteraction } from '../features/interactions/interactionSlice'

const initialState = {
  hcp_name: '',
  hcp_specialty: 'Cardiology',
  interaction_type: 'Detailing',
  channel: 'In-person',
  raw_notes: '',
  created_by: 'field-rep-demo'
}

export default function LogInteractionForm() {
  const dispatch = useDispatch()
  const [form, setForm] = useState(initialState)

  const update = (key, value) => setForm((prev) => ({ ...prev, [key]: value }))

  const onSubmit = async (e) => {
    e.preventDefault()
    await dispatch(createInteraction(form))
    setForm(initialState)
  }

  return (
    <form onSubmit={onSubmit} className="card form-grid">
      <h2>Structured Interaction Logging</h2>
      <input placeholder="HCP Name" value={form.hcp_name} onChange={(e) => update('hcp_name', e.target.value)} required />
      <input placeholder="Specialty" value={form.hcp_specialty} onChange={(e) => update('hcp_specialty', e.target.value)} required />
      <select value={form.interaction_type} onChange={(e) => update('interaction_type', e.target.value)}>
        <option>Detailing</option>
        <option>Sample Discussion</option>
        <option>Conference Follow-up</option>
      </select>
      <select value={form.channel} onChange={(e) => update('channel', e.target.value)}>
        <option>In-person</option>
        <option>Virtual</option>
        <option>Phone</option>
      </select>
      <textarea rows="5" placeholder="Write detailed notes" value={form.raw_notes} onChange={(e) => update('raw_notes', e.target.value)} required />
      <button type="submit">Save Interaction</button>
    </form>
  )
}
