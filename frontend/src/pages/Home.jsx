import { useEffect, useState } from 'react'
import API from '../api/api'
import JobCard from '../components/JobCard'


export default function Home(){
	const [jobs, setJobs] = useState([])
	const [q, setQ] = useState('')

	const fetchJobs = async (search) => {
		try{
			const res = await API.get('/jobs/search', { params: { q: search } })
			setJobs(res.data.results || [])
		}catch(e){
			setJobs([])
		}
	}

	useEffect(()=>{ fetchJobs() }, [])

	return (
		<div className="container mx-auto p-6">
			<div className="flex gap-2 mb-6">
				<input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search jobs" className="border p-2 flex-1" />
				<button onClick={()=>fetchJobs(q)} className="px-4 py-2 bg-indigo-600 text-white rounded">Search</button>
			</div>
			<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
				{jobs.map(j=> <JobCard key={j.id} job={j} />)}
			</div>
		</div>
	)
}