import React, { useEffect, useState } from 'react'
import { useSearchParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'


export default function LoginPage() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState(null)
    const { login, isLoggedIn } = useAuth()
    const [searchParams] = useSearchParams()
    const navigate = useNavigate()
    const next = searchParams.get('next') || '/'


    useEffect(() => {
        if (isLoggedIn) navigate(next)
    }, [isLoggedIn])


    const handleSubmit = async (e) => {
        e.preventDefault()
        setError(null)
        try {
            await login({ email, password })
            navigate(next)
        } catch (err) {
            setError(err?.response?.data?.message || 'Failed to login')
        }
    }


    return (
        <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
            <h2 className="text-xl font-bold mb-4">Log in</h2>
            {error && <div className="mb-3 text-red-600">{error}</div>}
            <form onSubmit={handleSubmit} className="space-y-3">
                <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full border rounded px-3 py-2" />
                <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" className="w-full border rounded px-3 py-2" />
                <button type="submit" className="w-full py-2 bg-indigo-600 text-white rounded">Login</button>
            </form>
            <p className="mt-4 text-sm">Don't have an account? <Link to="/signup" className="text-indigo-600">Sign up</Link></p>
        </div>
    )
}