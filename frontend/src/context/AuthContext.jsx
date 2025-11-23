import React, { createContext, useState, useEffect } from 'react'
import jwtDecode from 'jwt-decode'
import { useNavigate } from 'react-router-dom'


export const AuthContext = createContext()


export function AuthProvider({ children }){
const [user, setUser] = useState(null)
const nav = useNavigate()


useEffect(()=>{
const token = localStorage.getItem('token')
if (token){
try{ const p = jwtDecode(token); setUser({ id: p.sub, role: p.role }) }catch(e){ localStorage.removeItem('token') }
}
},[])


const login = (token) => {
localStorage.setItem('token', token)
const p = jwtDecode(token)
setUser({ id: p.sub, role: p.role })
if (p.role === 'recruiter') nav('/recruiter/dashboard')
else nav('/student/dashboard')
}


const logout = () => { localStorage.removeItem('token'); setUser(null); nav('/') }


return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>
}