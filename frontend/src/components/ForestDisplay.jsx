import './ForestDisplay.css'

function ForestDisplay({ logs }) {
  const recentLogs = logs.slice(0, 15)

  const getTreeSize = (points) => {
    if (points >= 50) return 'large'
    if (points >= 20) return 'medium'
    return 'small'
  }

  return (
    <div className="card forest-card grow">
      <div className="card-header">
        <h2 className="card-title">🌲 Your Forest</h2>
        <p className="card-subtitle">{logs.length} trees planted</p>
      </div>

      {logs.length === 0 ? (
        <div className="empty-forest">
          <div className="empty-icon">🌱</div>
          <h3>Start Your Forest</h3>
          <p>Complete your first task to plant a tree!</p>
        </div>
      ) : (
        <>
          <div className="forest-scene">
            <div className="sun">☀️</div>
            <div className="cloud">☁️</div>
            <div className="cloud cloud-2">☁️</div>
            
            <div className="forest-grid">
              {recentLogs.map((log, index) => {
                const row = Math.floor(index / 5)
                const col = index % 5
                
                return (
                  <div
                    key={log.id}
                    className={`tree-tile ${getTreeSize(log.points_earned)}`}
                    style={{
                      '--row': row,
                      '--col': col,
                      animationDelay: `${index * 0.1}s`
                    }}
                    title={`${log.task_text} - ${log.points_earned} pts`}
                  >
                    <div className="tile-diamond"></div>
                    <div className="tree">{log.tree_emoji}</div>
                  </div>
                )
              })}
            </div>
          </div>

          <div className="forest-logs">
            <h3>Recent Accomplishments</h3>
            <div className="log-list">
              {recentLogs.slice(0, 5).map((log) => (
                <div key={log.id} className="log-item">
                  <span className="log-tree">{log.tree_emoji}</span>
                  <div className="log-content">
                    <div className="log-text">{log.task_text}</div>
                    <div className="log-meta">
                      <span>{new Date(log.created_at).toLocaleDateString()}</span>
                      <span className="log-points">+{log.points_earned} pts</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default ForestDisplay
