import React, { useEffect, useMemo, useState } from 'react'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'


function SearchBar({ value, onChange, onSearch }) {
    return (
        <div className="flex justify-center mb-6">
            <input
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder="Search equipment, category or location..."
                className="border p-3 rounded-l-lg w-full max-w-2xl focus:outline-none"
            />
            <button onClick={onSearch} className="bg-indigo-600 text-white px-4 rounded-r-lg">Search</button>
        </div>
    )
}


export default function HomePage() {
    const [query, setQuery] = useState('')
    const [equipments, setEquipments] = useState([])
    const [loading, setLoading] = useState(true)
    const { isLoggedIn } = useAuth()
    const navigate = useNavigate()


    useEffect(() => {
        let mounted = true
        async function fetchList() {
            try {
                setLoading(true)
                const res = await api.get('/items')
                if (mounted) setEquipments(res.data || [])
            } catch (err) {
                console.error('failed to fetch listings', err)
            } finally {
                if (mounted) setLoading(false)
            }
        }
        fetchList()
        return () => (mounted = false)
    }, [])


    const filtered = useMemo(() => {
        if (!query) return equipments
        const q = query.toLowerCase()
        return equipments.filter((e) => (e.name || '').toLowerCase().includes(q) || (e.category || '').toLowerCase().includes(q))
    }, [query, equipments])


    const handleCardClick = (id) => {
        if (!isLoggedIn) {
            // redirect to login with a redirect back param
            navigate(`/login?next=/equipment/${id}`)
            return
        }
        navigate(`/equipment/${id}`)
    }


    return (
        <div>
            <div className="py-12 text-center">
                <h1 className="text-3xl font-bold text-gray-800">Rent the gear you need — fast.</h1>
                <p className="text-gray-600 mt-2">Cameras, drones, lights, and more. Short-term or long-term rentals.</p>
            </div>

            <SearchBar value={query} onChange={setQuery} onSearch={() => { }} />


            {loading ? (
                <div className="text-center py-12">Loading equipments…</div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {filtered.map((eq) => (
                        <div key={eq.id} className="bg-white rounded-lg shadow cursor-pointer hover:shadow-lg" onClick={() => handleCardClick(eq.id)}>
                            <div className="h-44 bg-gray-100 rounded-t-lg overflow-hidden flex items-center justify-center">
                                {eq.image ? (
                                    <img src={eq.image} alt={eq.name} className="object-cover h-full w-full" />
                                ) : (
                                    <div className="text-gray-400">No image</div>
                                )}
                            </div>
                            <div className="p-4">
                                <h3 className="font-semibold text-lg">{eq.name}</h3>
                                <p className="text-sm text-gray-500 truncate">{eq.description}</p>
                                <div className="mt-3 flex items-center justify-between">
                                    <div className="font-medium">₹{eq.price_per_day}/day</div>
                                    <div className="text-xs text-gray-500">{eq.location || '—'}</div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}