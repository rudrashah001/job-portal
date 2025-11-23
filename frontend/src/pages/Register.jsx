import { useState } from 'react'
import API from '../api/api'
import { useNavigate } from 'react-router-dom'


export default function Register(){
const [name,setName]=useState('')
const [email,setEmail]=useState('')
const [password,setPassword]=useState('')
const nav = useNavigate()


const submit = async (e)=>{
e.preventDefault()
await API.post('/students/register', { name, email, password })
nav('/login')
}


return (
<div className="container mx-auto p-6">
<form onSubmit={submit} className="max-w-md mx-auto bg-card p-6 rounded">
<h2 className="text-xl mb-4">Register (Student)</h2>
<input required value={name} onChange={e=>setName(e.target.value)} className="w-full p-2 mb-3 border" placeholder="Full name" />
<input required value={email} onChange={e=>setEmail(e.target.value)} className="w-full p-2 mb-3 border" placeholder="Email" />
<input required value={password} onChange={e=>setPassword(e.target.value)} type="password" className="w-full p-2 mb-3 border" placeholder="Password" />
<button className="w-full bg-indigo-600 text-white p-2 rounded">Create account</button>
</form>
</div>
)
}