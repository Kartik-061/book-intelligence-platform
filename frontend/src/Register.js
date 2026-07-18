import { useState } from "react";

export default function Register({ onClose, onSwitchToLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== password2) {
      setError("Passwords do not match");
      return;
    }
    const response = await fetch(
      "https://book-intelligence-platform.onrender.com/api/register/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      }
    );
    if (response.ok) {
      setSuccess(true);
    } else {
      const data = await response.json();
      setError(data.error || "Registration failed");
    }
  };

  return (
    <div style={{
      position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
      background: "rgba(0,0,0,0.7)", display: "flex",
      alignItems: "center", justifyContent: "center", zIndex: 1000
    }}>
      <div style={{
        background: "#1a1a2e", padding: "2rem", borderRadius: "12px",
        width: "350px", border: "1px solid #333"
      }}>
        <h2 style={{ color: "white", marginBottom: "1.5rem" }}>Register</h2>
        {success ? (
          <div>
            <p style={{ color: "#22c55e", marginBottom: "1rem" }}>Account created! Please login.</p>
            <button onClick={onSwitchToLogin} style={{
              width: "100%", padding: "0.75rem", background: "#6c63ff",
              color: "white", border: "none", borderRadius: "8px", cursor: "pointer"
            }}>Go to Login</button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            {error && <p style={{ color: "red", marginBottom: "1rem" }}>{error}</p>}
            <input type="text" placeholder="Username" value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ width: "100%", padding: "0.75rem", marginBottom: "1rem",
                borderRadius: "8px", border: "1px solid #444", background: "#0f0f23", color: "white" }}
            />
            <input type="password" placeholder="Password" value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ width: "100%", padding: "0.75rem", marginBottom: "1rem",
                borderRadius: "8px", border: "1px solid #444", background: "#0f0f23", color: "white" }}
            />
            <input type="password" placeholder="Confirm Password" value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              style={{ width: "100%", padding: "0.75rem", marginBottom: "1.5rem",
                borderRadius: "8px", border: "1px solid #444", background: "#0f0f23", color: "white" }}
            />
            <button type="submit" style={{
              width: "100%", padding: "0.75rem", background: "#6c63ff",
              color: "white", border: "none", borderRadius: "8px", cursor: "pointer", marginBottom: "1rem"
            }}>Register</button>
            <p style={{ color: "#94a3b8", textAlign: "center", cursor: "pointer" }}
              onClick={onSwitchToLogin}>Already have an account? Login</p>
          </form>
        )}
      </div>
    </div>
  );
}