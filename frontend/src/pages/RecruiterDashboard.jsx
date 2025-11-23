import { useEffect, useState } from 'react'
import API from '../api/api'
import { Link } from 'react-router-dom'


export default function RecruiterDashboard(){
const [posts, setPosts] = useState([])
useEffect(()=>{
API.get('/recruiters/my-posts').then(r=> setPosts(r.data.posts)).catch(()=>{})
},[])


return (
<div className="container mx-auto p-6">
<div className="flex justify-between items-center mb-6">
<h1 className="text-2xl">Recruiter Dashboard</h1>
<Link className="bg-indigo-600 text-white px-4 py-2 rounded" to="/post-job">Post Job</Link>
</div>
<div className="space-y-4">
{posts.map(p=> (
<div key={p.id} className="bg-card p-4 rounded shadow">
<h3 className="font-semibold">{p.title}</h3>
<p className="text-sm">Applicants: {p.applicants?.length || 0}</p>
</div>
))}
</div>
</div>
)
}