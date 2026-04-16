import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function QnA() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/history/').then(r => setHistory(r.data));
  }, []);

  const askQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/api/ask/', { question });
      setAnswer(res.data.answer);
      setHistory(prev => [{question, answer: res.data.answer, id: Date.now()}, ...prev]);
    } catch(e) { setAnswer('Error getting answer. Please try again.'); }
    setLoading(false);
  };

  return (
    <div style={{padding:'32px',maxWidth:'800px',margin:'0 auto'}}>
      <h1 style={{fontSize:'28px',fontWeight:'bold',marginBottom:'24px'}}>🤖 Ask AI about Books</h1>
      <div style={{background:'#1e293b',borderRadius:'16px',padding:'24px',marginBottom:'24px'}}>
        <textarea value={question} onChange={e=>setQuestion(e.target.value)}
          placeholder="Ask anything about books... e.g. 'Recommend a mystery book' or 'What is the highest rated book?'"
          style={{width:'100%',minHeight:'100px',background:'#0f172a',color:'white',border:'1px solid #334155',
            borderRadius:'8px',padding:'12px',fontSize:'14px',resize:'vertical',boxSizing:'border-box'}} />
        <button onClick={askQuestion} disabled={loading}
          style={{marginTop:'12px',background:'#6366f1',color:'white',border:'none',
            padding:'12px 24px',borderRadius:'8px',cursor:'pointer',fontSize:'16px',width:'100%'}}>
          {loading ? '⏳ Thinking...' : '🔍 Ask Question'}
        </button>
        {answer && (
          <div style={{marginTop:'20px',background:'#0f172a',borderRadius:'8px',padding:'16px'}}>
            <p style={{color:'#6366f1',fontWeight:'bold',marginBottom:'8px'}}>🤖 AI Answer:</p>
            <p style={{color:'white',lineHeight:'1.6'}}>{answer}</p>
          </div>
        )}
      </div>
      {history.length > 0 && (
        <div>
          <h2 style={{color:'white',marginBottom:'16px'}}>💬 Chat History</h2>
          {history.map(h => (
            <div key={h.id} style={{background:'#1e293b',borderRadius:'8px',padding:'16px',marginBottom:'12px'}}>
              <p style={{color:'#6366f1',fontWeight:'bold',marginBottom:'4px'}}>Q: {h.question}</p>
              <p style={{color:'#94a3b8',fontSize:'14px'}}>A: {h.answer?.substring(0,200)}...</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}