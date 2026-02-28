import { Link, useLocation } from 'react-router-dom'
import './Navbar.css'

function Navbar({ user, onLogout }) {
  const location = useLocation()

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-logo">
          <span className="logo-icon">🌲</span>
          <span className="logo-text">Done List</span>
        </Link>

        <div className="navbar-menu">
          <Link 
            to="/dashboard" 
            className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}
          >
            🏠 Dashboard
          </Link>
          <Link 
            to="/profile" 
            className={`nav-link ${location.pathname === '/profile' ? 'active' : ''}`}
          >
            👤 Profile
          </Link>
        </div>

        <div className="navbar-user">
          <div className="user-info">
            <span className="user-name">{user?.username}</span>
            <span className="user-level">Level {user?.current_level}</span>
          </div>
          <button onClick={onLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
