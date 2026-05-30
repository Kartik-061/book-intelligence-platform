export default function PrivacyPolicy() {
  return (
    <div style={{padding:'32px',maxWidth:'800px',margin:'0 auto',color:'white'}}>
      <h1 style={{fontSize:'28px',fontWeight:'bold',marginBottom:'24px'}}>Privacy Policy</h1>
      <p style={{color:'#94a3b8',marginBottom:'24px'}}>Last updated: May 2026</p>

      <section style={{marginBottom:'24px'}}>
        <h2 style={{fontSize:'20px',color:'#6366f1',marginBottom:'12px'}}>1. Data We Collect</h2>
        <p style={{lineHeight:'1.8',color:'#cbd5e1'}}>We collect your username and password (hashed) when you register. We also store your AI chat history (questions and answers) to provide chat history functionality.</p>
      </section>

      <section style={{marginBottom:'24px'}}>
        <h2 style={{fontSize:'20px',color:'#6366f1',marginBottom:'12px'}}>2. How We Use Your Data</h2>
        <p style={{lineHeight:'1.8',color:'#cbd5e1'}}>Your data is used solely to provide BookIQ services — authentication and personalized chat history. We do not sell or share your data with third parties.</p>
      </section>

      <section style={{marginBottom:'24px'}}>
        <h2 style={{fontSize:'20px',color:'#6366f1',marginBottom:'12px'}}>3. Data Storage</h2>
        <p style={{lineHeight:'1.8',color:'#cbd5e1'}}>Data is stored securely on Railway servers. Passwords are hashed using Django's built-in PBKDF2 algorithm and are never stored in plain text.</p>
      </section>

      <section style={{marginBottom:'24px'}}>
        <h2 style={{fontSize:'20px',color:'#6366f1',marginBottom:'12px'}}>4. Your Rights (DPDPA 2023)</h2>
        <p style={{lineHeight:'1.8',color:'#cbd5e1'}}>Under India's Digital Personal Data Protection Act 2023, you have the right to access, correct, and delete your personal data. To request deletion, contact us at krishkarthikyamotwani@gmail.com</p>
      </section>

      <section style={{marginBottom:'24px'}}>
        <h2 style={{fontSize:'20px',color:'#6366f1',marginBottom:'12px'}}>5. Cookies</h2>
        <p style={{lineHeight:'1.8',color:'#cbd5e1'}}>We use localStorage to store your JWT token for authentication. No tracking cookies are used.</p>
      </section>

      <section style={{marginBottom:'24px'}}>
        <h2 style={{fontSize:'20px',color:'#6366f1',marginBottom:'12px'}}>6. Contact</h2>
        <p style={{lineHeight:'1.8',color:'#cbd5e1'}}>For any privacy concerns: krishkarthikyamotwani@gmail.com</p>
      </section>
    </div>
  );
}