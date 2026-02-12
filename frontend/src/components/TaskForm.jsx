import { useState } from 'react'
import './TaskForm.css'

function TaskForm({ token, onSuccess }) {
  const [taskText, setTaskText] = useState('')
  const [effortLevel, setEffortLevel] = useState('sapling')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await fetch('/api/v1/logs', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          task_text: taskText,
          effort_level: effortLevel
        })
      })

      const data = await response.json()

      if (response.ok) {
        setMessage(`🎉 +${data.log.points_earned} points! ${data.level_up ? '⭐ Level Up!' : ''}`)
        setTaskText('')
        onSuccess()
        
        setTimeout(() => setMessage(''), 4000)
      } else {
        setMessage('Failed to log task')
      }
    } catch (error) {
      setMessage('Connection error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card task-form-card grow">
      <div className="card-header">
        <h2 className="card-title">✨ Complete a Task</h2>
        <p className="card-subtitle">Grow your forest one task at a time</p>
      </div>

      {message && (
        <div className={`alert ${message.includes('🎉') ? 'alert-success' : 'alert-error'}`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>What did you accomplish?</label>
          <textarea
            value={taskText}
            onChange={(e) => setTaskText(e.target.value)}
            placeholder="E.g., Completed morning workout, Finished project report..."
            required
            rows="3"
          />
        </div>

        <div className="effort-selector">
          <label>Effort Level</label>
          <div className="effort-options">
            <button
              type="button"
              className={`effort-btn ${effortLevel === 'seed' ? 'active' : ''}`}
              onClick={() => setEffortLevel('seed')}
            >
              <span className="effort-icon">🌱</span>
              <span className="effort-name">Seed</span>
              <span className="effort-points">8 pts</span>
            </button>

            <button
              type="button"
              className={`effort-btn ${effortLevel === 'sapling' ? 'active' : ''}`}
              onClick={() => setEffortLevel('sapling')}
            >
              <span className="effort-icon">🌿</span>
              <span className="effort-name">Sapling</span>
              <span className="effort-points">22-49 pts</span>
            </button>

            <button
              type="button"
              className={`effort-btn ${effortLevel === 'oak' ? 'active' : ''}`}
              onClick={() => setEffortLevel('oak')}
            >
              <span className="effort-icon">🌳</span>
              <span className="effort-name">Oak</span>
              <span className="effort-points">65 pts</span>
            </button>
          </div>
        </div>

        <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
          {loading ? 'Planting...' : '🌲 Plant Tree'}
        </button>
      </form>
    </div>
  )
}

export default TaskForm
