import { useAuth } from "./AuthContext";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const { token } = useAuth();
  
  if (!token) {
    alert("Please login to use Ask AI!");
    return <Navigate to="/" replace />;
  }
  
  return children;
}