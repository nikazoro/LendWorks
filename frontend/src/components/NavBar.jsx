import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'


export default function Navbar() {
    const { user, isLoggedIn, logout } = useAuth()
    const navigate = useNavigate()


    return (
        <header className="bg-white shadow">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    <div className="flex items-center">
                        <Link to="/" className="text-xl font-bold text-indigo-600">Rental Gears</Link>
                    </div>


                    <div className="flex-1 px-4">
                        {/* Could put global search here if desired */}
                    </div>


                    <div className="flex items-center space-x-4">
                        <Link to="/" className="text-sm text-gray-600 hover:text-gray-900">Home</Link>
                        {isLoggedIn ? (
                            <div className="flex items-center space-x-3">
                                <button
                                    onClick={() => navigate('/profile')}
                                    className="flex items-center gap-2 text-sm"
                                >
                                    <div className="w-8 h-8 rounded-full bg-indigo-200 flex items-center justify-center text-indigo-700">{user?.full_name?.[0] || 'U'}</div>
                                    <span className="hidden sm:inline">{user?.full_name}</span>
                                </button>
                                <button onClick={logout} className="text-sm text-red-500">Logout</button>
                            </div>
                        ) : (
                            <div className="flex items-center gap-2">
                                <Link to="/login" className="text-sm px-3 py-1 border rounded">Login</Link>
                                <Link to="/signup" className="text-sm px-3 py-1 bg-indigo-600 text-white rounded">Sign up</Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </header>
    )
}