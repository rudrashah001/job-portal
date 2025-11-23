import { Link } from 'react-router-dom'
export default function JobCard({job}){
return (
<div className="bg-card p-4 rounded shadow-sm">
<h3 className="text-lg font-semibold">{job.title}</h3>
<p className="text-sm">{job.company_name} • {job.location}</p>
<p className="mt-2 text-sm">{job.description?.slice(0,150)}...</p>
<div className="mt-3">
<Link to={`/job/${job.id}`} className="text-indigo-600">View</Link>
</div>
</div>
)
}