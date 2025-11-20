import React, { createContext, useContext, useEffect, useState } from 'react'
import api from '../api/axios'
import { useNavigate } from 'react-router-dom'


const AuthContext = createContext(null)


export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()


    useEffect(() => {
        // Try to fetch current user. If backend uses cookie-based auth, this will validate it.
        async function fetchMe() {
            try {
                const token = localStorage.getItem('token')
                if (!token) {
                    setLoading(false)
                    return
                }
                const res = await api.get('/users/me')
                setUser(res.data)
            } catch (err) {
                console.warn('Auth check failed', err?.response?.status)
                localStorage.removeItem('token')
                setUser(null)
            } finally {
                setLoading(false)
            }
        }
        fetchMe()
    }, [])


    const login = async ({ email, password }) => {
        const res = await api.post('/auth/login', { email, password })
        // backend should return { token, user }
        if (res.data?.token) {
            localStorage.setItem('token', res.data.token)
        }
        if (res.data?.user) setUser(res.data.user)
        return res.data
    }


    const signup = async ({ full_name, email, password }) => {
        const res = await api.post('/auth/signup', { full_name, email, password })
        if (res.data?.token) localStorage.setItem('token', res.data.token)
        if (res.data?.user) setUser(res.data.user)
        return res.data
    }

    const logout = async () => {
        try {
            await api.post('/auth/logout')
        } catch (err) {
            // ignore
        }
        localStorage.removeItem('token')
        setUser(null)
        navigate('/')
    }


    return (
        <AuthContext.Provider value={{ user, loading, login, signup, logout, isLoggedIn: !!user }}>
            {children}
        </AuthContext.Provider>
    )
}


export function useAuth() {
    return useContext(AuthContext)
}