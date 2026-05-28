import { useState } from "react";
import { useAuth } from "./AuthContext";

export default function Login({ onClose }) {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await login(username, password);
    if (success) {
      onClose();
    } else {
      setError("Invalid username or password");
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
        <h2 style={{ color: "white", marginBottom: "1.5rem" }}>Login</h2>
        {error && <p style={{ color: "red", marginBottom: "1rem" }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="text" placeholder="Username"
            value={username} onChange={(e) => setUsername(e.target.value)}
            style={{ width: "100%", padding: "0.75rem", marginBottom: "1rem",
              borderRadius: "8px", border: "1px solid #444", background: "#0f0f23",
              color: "white" }}
          />
          <input
            type="password" placeholder="Password"
            value={password} onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", padding: "0.75rem", marginBottom: "1.5rem",
              borderRadius: "8px", border: "1px solid #444", background: "#0f0f23",
              color: "white" }}
          />
          <button type="submit" style={{
            width: "100%", padding: "0.75rem", background: "#6c63ff",
            color: "white", border: "none", borderRadius: "8px", cursor: "pointer"
          }}>
            Login
          </button>
        </form>
      </div>
    </div>
  );
}