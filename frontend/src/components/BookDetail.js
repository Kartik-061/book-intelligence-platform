import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

export default function BookDetail() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/books/${id}/`).then(r => setBook(r.data));
    axios.get(`http://localhost:8000/api/books/${id}/recommend/`).then(r => setRecs(r.data));
  }, [id]);

  if (!book) return <p style={{color:'white',padding:'32px'}}>Loading...</p>;

  return (
    <div style={{padding:'32px',maxWidth:'900px',margin:'0 auto'}}>
      <Link to="/" style={{color:'#6366f1',textDecoration:'none',marginBottom:'16px',display:'block'}}>← Back</Link>
      <div style={{display:'flex',gap:'32px',background:'#1e293b',borderRadius:'16px',padding:'24px'}}>
        <img src={book.cover_image} alt={book.title}
          style={{width:'200px',height:'280px',objectFit:'cover',borderRadius:'8px'}}
          onError={e=>e.target.src='https://via.placeholder.com/200x300?text=Book'} />
        <div style={{flex:1}}>
          <h1 style={{fontSize:'24px',fontWeight:'bold',color:'white',marginBottom:'8px'}}>{book.title}</h1>
          <p style={{color:'#6366f1',marginBottom:'8px'}}>{book.ai_genre || book.genre}</p>
          <p style={{color:'#fbbf24',marginBottom:'8px'}}>⭐ {book.rating}/5</p>
          <p style={{color:'#10b981',marginBottom:'16px'}}>{book.price}</p>
          <div style={{background:'#0f172a',borderRadius:'8px',padding:'16px',marginBottom:'16px'}}>
            <p style={{color:'#94a3b8',fontSize:'13px',fontWeight:'bold',marginBottom:'8px'}}>🤖 AI Summary</p>
            <p style={{color:'white',fontSize:'14px'}}>{book.ai_summary}</p>
          </div>
          <div style={{background:'#0f172a',borderRadius:'8px',padding:'16px',marginBottom:'16px'}}>
            <p style={{color:'#94a3b8',fontSize:'13px',fontWeight:'bold',marginBottom:'8px'}}>😊 Sentiment</p>
            <span style={{background: book.sentiment==='Positive'?'#10b981':'#f59e0b',
              color:'white',padding:'4px 12px',borderRadius:'20px',fontSize:'13px'}}>{book.sentiment}</span>
          </div>
          <div style={{background:'#0f172a',borderRadius:'8px',padding:'16px'}}>
            <p style={{color:'#94a3b8',fontSize:'13px',fontWeight:'bold',marginBottom:'8px'}}>📖 Description</p>
            <p style={{color:'white',fontSize:'14px'}}>{book.description}</p>
          </div>
        </div>
      </div>
      {recs.length > 0 && (
        <div style={{marginTop:'32px'}}>
          <h2 style={{color:'white',marginBottom:'16px'}}>📚 You might also like</h2>
          <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:'16px'}}>
            {recs.map(r => (
              <Link to={`/book/${r.id}`} key={r.id} style={{textDecoration:'none'}}>
                <div style={{background:'#1e293b',borderRadius:'8px',padding:'12px',textAlign:'center'}}>
                  <img src={r.cover_image} alt={r.title}
                    style={{width:'100%',height:'120px',objectFit:'cover',borderRadius:'4px',marginBottom:'8px'}}
                    onError={e=>e.target.src='https://via.placeholder.com/150x200?text=Book'} />
                  <p style={{color:'white',fontSize:'12px',fontWeight:'bold'}}>{r.title.substring(0,30)}...</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}