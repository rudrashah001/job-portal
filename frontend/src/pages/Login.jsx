import { useState, useContext } from 'react'
import API from '../api/api'
import { AuthContext } from '../context/AuthContext'


export default function Login(){
const [email,setEmail] = useState('')
const [password,setPassword] = useState('')
const { login } = useContext(AuthContext)


const submit = async (e)=>{
e.preventDefault()
const res = await API.post('/students/login', { email, password })
login(res.data.access_token)
}


return (
<div className="container mx-auto p-6">
<form onSubmit={submit} className="max-w-md mx-auto bg-card p-6 rounded">
<h2 className="text-xl mb-4">Login</h2>
<input required value={email} onChange={e=>setEmail(e.target.value)} className="w-full p-2 mb-3 border" placeholder="Email" />
<input required value={password} onChange={e=>setPassword(e.target.value)} type="password" className="w-full p-2 mb-3 border" placeholder="Password" />
<button className="w-full bg-indigo-600 text-white p-2 rounded">Login</button>
</form>
</div>
)
}