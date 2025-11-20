import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import { useAuth } from '../context/AuthContext'


export default function EquipmentDetail() {
    const { id } = useParams()
    const [item, setItem] = useState(null)
    const [loading, setLoading] = useState(true)
    const { isLoggedIn } = useAuth()
    const navigate = useNavigate()


    useEffect(() => {
        let mounted = true
        async function fetchItem() {
            try {
                setLoading(true)
                const res = await api.get(`/items/${id}`)
                if (mounted) setItem(res.data)
            } catch (err) {
                console.error(err)
            } finally {
                if (mounted) setLoading(false)
            }
        }
        fetchItem()
        return () => (mounted = false)
    }, [id])


    const handleBook = () => {
        if (!isLoggedIn) return navigate(`/login?next=/equipment/${id}`)
        // otherwise proceed to booking flow (not implemented here)
        alert('Booking flow — implement on your backend')
    }


    if (loading) return <div>Loading…</div>
    if (!item) return <div className="text-center py-12">Item not found.</div>


    return (
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="h-96 bg-gray-100 flex items-center justify-center rounded">
                    {item.image ? <img src={item.image} alt={item.name} className="object-contain h-full" /> : <div>No image</div>}
                </div>
                <div>
                    <h2 className="text-2xl font-bold">{item.name}</h2>
                    <p className="text-gray-600 mt-2">{item.description}</p>
                    <div className="mt-4">
                        <div className="text-xl font-semibold">₹{item.price_per_day} / day</div>
                        <div className="mt-4">
                            <button onClick={handleBook} className="px-4 py-2 bg-indigo-600 text-white rounded">Book now</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}