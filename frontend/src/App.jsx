import React from 'react'
import Header from './components/Header'
import Home from './pages/home'

export default function App(){
  return (
    <div>
      <Header />
      <main className="min-h-[calc(100vh-4rem)]">
        <Home />
      </main>
    </div>
  )
}

