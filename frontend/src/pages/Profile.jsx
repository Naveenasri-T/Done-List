import { useState } from 'react'
import Navbar from '../components/Navbar'
import './Profile.css'

function Profile({ token, user, setUser, onLogout }) {
  const [isEditing, setIsEditing] = useState(false)
  const [bio, setBio] = useState(user?.bio || '')
  const [isPublic, setIsPublic] = useState(user?.is_public || false)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleUpdate = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const response = await fetch('/api/v1/auth/me', {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bio, is_public: isPublic })
      })

      if (response.ok) {
        const data = await response.json()
        setUser(data)
        setMessage('Profile updated successfully! ✓')
        setIsEditing(false)
      } else {
        setMessage('Failed to update profile')
      }
    } catch (error) {
      setMessage('Connection error')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (format) => {
    try {
      const response = await fetch(`/api/v1/export/${format}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `forest-data.${format}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }
    } catch (error) {
      console.error('Export failed:', error)
    }
  }

  return (
    <div className="profile-container fade-in">
      <Navbar user={user} onLogout={onLogout} />
      
      <main className="profile-main">
        <div className="profile-grid">
          {/* Profile Info Card */}
          <div className="card grow">
            <div className="profile-header-section">
              <div className="profile-avatar">
                {user?.username?.charAt(0).toUpperCase() || '🌲'}
              </div>
              <div className="profile-info">
                <h2>{user?.username}</h2>
                <p className="profile-email">{user?.email}</p>
                <div className="profile-badges">
                  <span className="badge">Level {user?.current_level}</span>
                  <span className="badge badge-gold">{user?.total_points} Points</span>
                </div>
              </div>
            </div>

            {message && (
              <div className={`alert ${message.includes('✓') ? 'alert-success' : 'alert-error'}`}>
                {message}
              </div>
            )}

            {isEditing ? (
              <form onSubmit={handleUpdate} className="profile-form">
                <div className="input-group">
                  <label>Bio</label>
                  <textarea
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    placeholder="Tell us about your forest journey..."
                    rows="3"
                  />
                </div>

                <div className="profile-toggle">
                  <label className="toggle-label">
                    <input
                      type="checkbox"
                      checked={isPublic}
                      onChange={(e) => setIsPublic(e.target.checked)}
                    />
                    <span className="toggle-slider"></span>
                    <span className="toggle-text">Public Profile (allows sharing)</span>
                  </label>
                </div>

                <div className="button-group">
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Saving...' : 'Save Changes'}
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setIsEditing(false)}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <div className="profile-view">
                {bio && (
                  <div className="profile-bio">
                    <strong>Bio:</strong>
                    <p>{bio}</p>
                  </div>
                )}
                <div className="profile-status">
                  <span className={`status-badge ${isPublic ? 'status-public' : 'status-private'}`}>
                    {isPublic ? '🌍 Public Profile' : '🔒 Private Profile'}
                  </span>
                </div>
                <button className="btn btn-primary" onClick={() => setIsEditing(true)}>
                  Edit Profile
                </button>
              </div>
            )}
          </div>

          {/* Export Data Card */}
          <div className="card grow">
            <div className="card-header">
              <h3 className="card-title">📊 Export Your Data</h3>
              <p className="card-subtitle">Download your forest progress</p>
            </div>

            <div className="export-options">
              <button className="export-btn" onClick={() => handleExport('json')}>
                <span className="export-icon">📄</span>
                <div>
                  <strong>JSON Format</strong>
                  <p>Complete data with all details</p>
                </div>
              </button>

              <button className="export-btn" onClick={() => handleExport('csv')}>
                <span className="export-icon">📊</span>
                <div>
                  <strong>CSV Format</strong>
                  <p>Spreadsheet-friendly format</p>
                </div>
              </button>
            </div>
          </div>

          {/* Stats Summary Card */}
          <div className="card grow">
            <div className="card-header">
              <h3 className="card-title">🌟 Your Journey</h3>
            </div>

            <div className="stats-summary">
              <div className="stat-item">
                <div className="stat-icon">🏆</div>
                <div>
                  <div className="stat-value">{user?.current_level}</div>
                  <div className="stat-label">Current Level</div>
                </div>
              </div>

              <div className="stat-item">
                <div className="stat-icon">⭐</div>
                <div>
                  <div className="stat-value">{user?.total_points}</div>
                  <div className="stat-label">Total Points</div>
                </div>
              </div>

              <div className="stat-item">
                <div className="stat-icon">🌱</div>
                <div>
                  <div className="stat-value">
                    {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                  </div>
                  <div className="stat-label">Member Since</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Profile
