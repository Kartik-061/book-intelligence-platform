import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import BookList from './components/BookList';
import BookDetail from './components/BookDetail';
import QnA from './components/QnA';
import { AuthProvider, useAuth } from './AuthContext';
import ProtectedRoute from './ProtectedRoute';
import Register from './Register';
import Login from './Login';
import './App.css';

function NavBar() {
  const { token, logout } = useAuth();
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  return (
    <>
      <nav style={{background:'#1e293b',padding:'16px 32px',display:'flex',gap:'24px',alignItems:'center'}}>
        <span style={{fontSize:'20px',fontWeight:'bold',color:'#6366f1'}}>📚 BookIQ</span>
        <Link to="/" style={{color:'#94a3b8',textDecoration:'none'}}>Home</Link>
        <Link to="/qa" style={{color:'#94a3b8',textDecoration:'none'}}>Ask AI</Link>
        <div style={{marginLeft:'auto', display:'flex', gap:'8px'}}>
          {token ? (
            <button onClick={logout} style={{padding:'8px 16px',background:'#ef4444',color:'white',border:'none',borderRadius:'8px',cursor:'pointer'}}>
              Logout
            </button>
          ) : (
            <>
              <button onClick={() => setShowLogin(true)} style={{padding:'8px 16px',background:'#6c63ff',color:'white',border:'none',borderRadius:'8px',cursor:'pointer'}}>
                Login
              </button>
              <button onClick={() => setShowRegister(true)} style={{padding:'8px 16px',background:'#22c55e',color:'white',border:'none',borderRadius:'8px',cursor:'pointer'}}>
                Register
              </button>
            </>
          )}
        </div>
      </nav>
      {showLogin && <Login onClose={() => setShowLogin(false)} />}
      {showRegister && <Register onClose={() => setShowRegister(false)} onSwitchToLogin={() => { setShowRegister(false); setShowLogin(true); }} />}
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div style={{minHeight:'100vh',background:'#0f172a',color:'white'}}>
          <NavBar />
          <Routes>
            <Route path="/" element={<BookList />} />
            <Route path="/book/:id" element={<BookDetail />} />
            <Route path="/qa" element={
              <ProtectedRoute>
                <QnA />
            </ProtectedRoute>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;