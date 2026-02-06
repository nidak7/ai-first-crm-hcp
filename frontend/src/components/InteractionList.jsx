import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchInteractions } from '../features/interactions/interactionSlice'

export default function InteractionList() {
  const dispatch = useDispatch()
  const { items, loading } = useSelector((state) => state.interactions)

  useEffect(() => {
    dispatch(fetchInteractions())
  }, [dispatch])

  return (
    <div className="card">
      <h2>Recent HCP Interactions</h2>
      {loading && <p>Loading...</p>}
      {!loading && items.length === 0 && <p>No interactions logged yet.</p>}
      <div className="list">
        {items.map((item) => (
          <article key={item.id} className="list-item">
            <h3>{item.hcp_name} <span>{item.hcp_specialty}</span></h3>
            <p><strong>Summary:</strong> {item.summary}</p>
            <p><strong>Sentiment:</strong> {item.sentiment}</p>
            <p><strong>Follow-up:</strong> {item.follow_up_action}</p>
          </article>
        ))}
      </div>
    </div>
  )
}
