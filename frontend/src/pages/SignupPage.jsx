import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'


export default function SignupPage() {
    const [full_name, setFullName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState(null)
    const { signup, isLoggedIn } = useAuth()
    const navigate = useNavigate()


    useEffect(() => {
        if (isLoggedIn) navigate('/')
    }, [isLoggedIn])


    const handleSubmit = async (e) => {
        e.preventDefault()
        setError(null)
        try {
            await signup({ full_name, email, password })
            navigate('/')
        } catch (err) {
            setError(err?.response?.data?.message || 'Failed to sign up')
        }
    }


    return (
        <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
            <h2 className="text-xl font-bold mb-4">Create account</h2>
            {error && <div className="mb-3 text-red-600">{error}</div>}
            <form onSubmit={handleSubmit} className="space-y-3">
                <input value={full_name} onChange={(e) => setFullName(e.target.value)} placeholder="Full name" className="w-full border rounded px-3 py-2" />
                <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full border rounded px-3 py-2" />
                <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" className="w-full border rounded px-3 py-2" />
                <button type="submit" className="w-full py-2 bg-indigo-600 text-white rounded">Sign up</button>
            </form>
        </div>
    )
}