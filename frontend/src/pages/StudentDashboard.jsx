import { useEffect, useState } from 'react'
import API from '../api/api'


export default function StudentDashboard(){
const [applied, setApplied] = useState([])


useEffect(()=>{
// example: fetch applications for current student
API.get('/students/me').then(r=>console.log(r.data)).catch(()=>{})
// implement call to fetch student's applications if backend supports
},[])


return (
<div className="container mx-auto p-6">
<h1 className="text-2xl mb-4">Student Dashboard</h1>
<p>Applied jobs list will show here.</p>
</div>
)
}