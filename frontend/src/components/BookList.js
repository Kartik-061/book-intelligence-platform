import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function BookList() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);

  useEffect(() => { fetchBooks(); }, []);

  const fetchBooks = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/books/');
      setBooks(res.data);
    } catch(e) { console.error(e); }
    setLoading(false);
  };

  const scrapeBooks = async () => {
    setScraping(true);
    try {
      await axios.post('http://localhost:8000/api/books/upload/');
      await fetchBooks();
    } catch(e) { console.error(e); }
    setScraping(false);
  };

  return (
    <div style={{padding:'32px'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'24px'}}>
        <h1 style={{fontSize:'28px',fontWeight:'bold'}}>Book Library</h1>
        <button onClick={scrapeBooks} disabled={scraping}
          style={{background:'#6366f1',color:'white',border:'none',padding:'10px 20px',borderRadius:'8px',cursor:'pointer',fontSize:'16px'}}>
          {scraping ? '⏳ Scraping...' : '🔄 Fetch Books'}
        </button>
      </div>
      {loading && <p style={{color:'#94a3b8'}}>Loading...</p>}
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(200px,1fr))',gap:'20px'}}>
        {books.map(book => (
          <Link to={`/book/${book.id}`} key={book.id} style={{textDecoration:'none'}}>
            <div style={{background:'#1e293b',borderRadius:'12px',overflow:'hidden',transition:'transform 0.2s'}}
              onMouseOver={e=>e.currentTarget.style.transform='scale(1.03)'}
              onMouseOut={e=>e.currentTarget.style.transform='scale(1)'}>
              <img src={book.cover_image} alt={book.title}
                style={{width:'100%',height:'200px',objectFit:'cover'}}
                onError={e=>e.target.src='https://via.placeholder.com/200x300?text=Book'} />
              <div style={{padding:'12px'}}>
                <p style={{fontWeight:'bold',fontSize:'14px',color:'white',marginBottom:'4px',
                  overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{book.title}</p>
                <p style={{color:'#6366f1',fontSize:'12px',marginBottom:'4px'}}>{book.ai_genre || book.genre}</p>
                <p style={{color:'#fbbf24',fontSize:'12px'}}>{'⭐'.repeat(Math.round(book.rating || 0))} {book.rating}/5</p>
                <p style={{color:'#10b981',fontSize:'12px'}}>{book.price}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
      {books.length === 0 && !loading && (
        <div style={{textAlign:'center',marginTop:'80px',color:'#94a3b8'}}>
          <p style={{fontSize:'48px'}}>📚</p>
          <p style={{fontSize:'18px'}}>No books yet. Click "Fetch Books" to scrape!</p>
        </div>
      )}
    </div>
  );
}