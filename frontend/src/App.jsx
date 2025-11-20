import React from 'react'
import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import EquipmentDetail from './pages/EquipmentDetail'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import Navbar from './components/Navbar'


export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/equipment/:id" element={<EquipmentDetail />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
        </Routes>
      </main>
    </div>
  )
}