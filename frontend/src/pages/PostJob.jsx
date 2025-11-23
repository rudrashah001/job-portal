import { useState } from 'react'
import API from '../api/api'
import { useNavigate } from 'react-router-dom'


export default function PostJob(){
const [title,setTitle] = useState('')
const [description,setDescription] = useState('')
const [company_name,setCompany] = useState('')
const [location,setLocation] = useState('')
const nav = useNavigate()


const submit = async (e)=>{
e.preventDefault()
await API.post('/jobs/post', { title, description, company_name, location })
nav('/recruiter/dashboard')
}


return (
<div className="container mx-auto p-6">
<form onSubmit={submit} className="max-w-xl bg-card p-6 rounded">
<h2 className="text-xl mb-4">Post a Job</h2>
<input className="w-full p-2 mb-3 border" value={title} onChange={e=>setTitle(e.target.value)} placeholder="Job title" required />
<input className="w-full p-2 mb-3 border" value={company_name} onChange={e=>setCompany(e.target.value)} placeholder="Company name" required />
<input className="w-full p-2 mb-3 border" value={location} onChange={e=>setLocation(e.target.value)} placeholder="Location" />
<textarea className="w-full p-2 mb-3 border" value={description} onChange={e=>setDescription(e.target.value)} placeholder="Job description" rows={6} />
<button className="bg-indigo-600 text-white px-4 py-2 rounded">Post Job</button>
</form>
</div>
)
}