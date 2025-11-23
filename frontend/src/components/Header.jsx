import { Link } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'


export default function Header(){
const { user, logout } = useContext(AuthContext)
return (
<header className="bg-white shadow-sm p-4" data-theme>
<div className="container mx-auto flex justify-between items-center">
<div className="text-xl font-bold"><Link to="/">JobPortal</Link></div>
<nav className="space-x-4">
<Link to="/">Home</Link>
{!user && <><Link to="/login">Login</Link><Link to="/register">Register</Link></>}
{user && user.role==='student' && <Link to="/student/dashboard">Dashboard</Link>}
{user && user.role==='recruiter' && <Link to="/recruiter/dashboard">Recruiter</Link>}
{user && <button onClick={logout} className="ml-2">Logout</button>}
</nav>
</div>
</header>
)
}