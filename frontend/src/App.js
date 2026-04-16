import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import BookList from './components/BookList';
import BookDetail from './components/BookDetail';
import QnA from './components/QnA';
import './App.css';

function App() {
  return (
    <Router>
      <div style={{minHeight:'100vh',background:'#0f172a',color:'white'}}>
        <nav style={{background:'#1e293b',padding:'16px 32px',display:'flex',gap:'24px',alignItems:'center'}}>
          <span style={{fontSize:'20px',fontWeight:'bold',color:'#6366f1'}}>📚 BookIQ</span>
          <Link to="/" style={{color:'#94a3b8',textDecoration:'none'}}>Home</Link>
          <Link to="/qa" style={{color:'#94a3b8',textDecoration:'none'}}>Ask AI</Link>
        </nav>
        <Routes>
          <Route path="/" element={<BookList />} />
          <Route path="/book/:id" element={<BookDetail />} />
          <Route path="/qa" element={<QnA />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;