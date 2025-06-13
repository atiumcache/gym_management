import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router'
import { Home } from './pages/Home'
import { Dashboard } from './pages/Dashboard'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/dashboard' element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
};

export default App
