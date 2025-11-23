import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import API from '../api/api'


export default function JobDetails(){
const { id } = useParams()
const [job, setJob] = useState(null)
const [applied, setApplied] = useState(false)


useEffect(()=>{
API.get(`/jobs/${id}`).then(r=> setJob(r.data)).catch(()=>{})
},[id])


const apply = async ()=>{
try{
const res = await API.post(`/jobs/${id}/apply`)
alert('Applied successfully')
setApplied(true)
}catch(e){ alert('Apply failed') }
}


if(!job) return <div className="p-6">Loading...</div>
return (
<div className="container mx-auto p-6">
<h1 className="text-2xl mb-2">{job.title}</h1>
<p className="text-sm mb-4">{job.company_name} • {job.location}</p>
<div className="bg-card p-4 rounded mb-4">{job.description}</div>
<button onClick={apply} className="bg-indigo-600 text-white px-4 py-2 rounded" disabled={applied}>Apply</button>
</div>
)
}