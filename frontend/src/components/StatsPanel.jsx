import './StatsPanel.css'

function StatsPanel({ user, streaks, todayStats }) {
  return (
    <div className="card stats-panel grow">
      <div className="stats-grid">
        {/* Today's Progress */}
        <div className="stat-card today">
          <div className="stat-header">
            <span className="stat-emoji">📅</span>
            <span className="stat-title">Today</span>
          </div>
          <div className="stat-value">{todayStats.logs.length}</div>
          <div className="stat-label">Tasks</div>
          <div className="stat-subvalue">{todayStats.points} points</div>
        </div>

        {/* Level */}
        <div className="stat-card level">
          <div className="stat-header">
            <span className="stat-emoji">🏆</span>
            <span className="stat-title">Level</span>
          </div>
          <div className="stat-value">{user?.current_level || 1}</div>
          <div className="stat-label">Current</div>
          <div className="stat-subvalue">{user?.total_points || 0} points</div>
        </div>

        {/* Daily Streak */}
        <div className="stat-card streak">
          <div className="stat-header">
            <span className="stat-emoji">🔥</span>
            <span className="stat-title">Streak</span>
          </div>
          <div className="stat-value">{streaks?.daily?.current_count || 0}</div>
          <div className="stat-label">Days</div>
          <div className="stat-subvalue">
            Best: {streaks?.daily?.longest_count || 0}
          </div>
        </div>

        {/* Weekly */}
        <div className="stat-card weekly">
          <div className="stat-header">
            <span className="stat-emoji">📊</span>
            <span className="stat-title">Weekly</span>
          </div>
          <div className="stat-value">{streaks?.weekly?.current_count || 0}</div>
          <div className="stat-label">Weeks</div>
          <div className="stat-subvalue">
            Best: {streaks?.weekly?.longest_count || 0}
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatsPanel
