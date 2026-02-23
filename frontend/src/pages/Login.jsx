import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useGoogleLogin } from '@react-oauth/google'
import API_BASE_URL from '../config/api'
import './Auth.css'

function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [googleLoading, setGoogleLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      const data = await response.json()

      if (response.ok) {
        onLogin(data.access_token, data.user)
      } else {
        setError(data.detail || 'Login failed')
      }
    } catch (err) {
      setError('Connection error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleSuccess = async (tokenResponse) => {
    setGoogleLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: tokenResponse.access_token })
      })
      const data = await res.json()
      if (res.ok) {
        onLogin(data.access_token, data.user)
      } else {
        setError(data.detail || 'Google login failed')
      }
    } catch (err) {
      setError('Connection error. Please try again.')
    } finally {
      setGoogleLoading(false)
    }
  }

  const googleLogin = useGoogleLogin({
    onSuccess: handleGoogleSuccess,
    onError: () => setError('Google login failed. Please try again.'),
    flow: 'implicit',
    ux_mode: 'popup',
  })

  return (
    <div className="auth-container fade-in">
      <div className="auth-card grow">
        <div className="auth-header">
          <div className="forest-icon">🌲</div>
          <h1>Welcome Back</h1>
          <p>Continue your forest journey</p>
        </div>

        {error && (
          <div className="alert alert-error">
            <span>⚠️</span>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="auth-divider">
          <span>or</span>
        </div>

        <button
          className="btn btn-google btn-full"
          onClick={() => googleLogin()}
          disabled={googleLoading}
          type="button"
        >
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" width="20" height="20" />
          {googleLoading ? 'Connecting...' : 'Continue with Google'}
        </button>

        <div className="auth-footer">
          <p>
            Don't have an account?{' '}
            <Link to="/register" className="auth-link">Create one</Link>
          </p>
        </div>
      </div>

      <div className="auth-background">
        <div className="tree-emoji">🌱</div>
        <div className="tree-emoji">🌿</div>
        <div className="tree-emoji">🌲</div>
        <div className="tree-emoji">🌳</div>
      </div>
    </div>
  )
}

export default Login
