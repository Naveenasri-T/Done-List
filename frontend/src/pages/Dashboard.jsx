import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import TaskForm from '../components/TaskForm'
import ForestDisplay from '../components/ForestDisplay'
import StatsPanel from '../components/StatsPanel'
import './Dashboard.css'

function Dashboard({ token, user, onLogout }) {
  const [logs, setLogs] = useState([])
  const [streaks, setStreaks] = useState(null)
  const [todayStats, setTodayStats] = useState({ logs: [], points: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const headers = { 'Authorization': `Bearer ${token}` }
      
      const [logsRes, streaksRes, todayRes] = await Promise.all([
        fetch('/api/v1/logs', { headers }),
        fetch('/api/v1/streaks', { headers }),
        fetch('/api/v1/logs/today', { headers })
      ])

      if (logsRes.ok) {
        const logsData = await logsRes.json()
        setLogs(logsData)
      }

      if (streaksRes.ok) {
        const streaksData = await streaksRes.json()
        setStreaks(streaksData)
      }

      if (todayRes.ok) {
        const todayData = await todayRes.json()
        const points = todayData.reduce((sum, log) => sum + log.points_earned, 0)
        setTodayStats({ logs: todayData, points })
      }
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleTaskComplete = () => {
    fetchData()
  }

  if (loading) {
    return (
      <>
        <Navbar user={user} onLogout={onLogout} />
        <div className="spinner"></div>
      </>
    )
  }

  return (
    <div className="dashboard-container fade-in">
      <Navbar user={user} onLogout={onLogout} />
      
      <main className="dashboard-main">
        <div className="dashboard-grid">
          {/* Left Column - Task Entry */}
          <div className="dashboard-left">
            <TaskForm token={token} onSuccess={handleTaskComplete} />
            <StatsPanel user={user} streaks={streaks} todayStats={todayStats} />
          </div>

          {/* Right Column - Forest Display */}
          <div className="dashboard-right">
            <ForestDisplay logs={logs} />
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
