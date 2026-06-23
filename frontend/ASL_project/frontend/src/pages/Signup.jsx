import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = () => {
    if (email && password) {
      alert("Account created!");
      navigate("/");
    } else {
      alert("Fill all fields");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Create Account</h1>

        <input
          type="text"
          placeholder="Email"
          style={styles.input}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          style={styles.input}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.button} onClick={handleSignup}>
          Sign Up
        </button>

        <p style={styles.link} onClick={() => navigate("/")}>
          Already have an account? Login
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    fontFamily: "Poppins, sans-serif",
  },
  card: {
    background: "#111827",
    padding: "30px",
    borderRadius: "10px",
    width: "300px",
    boxShadow: "0px 4px 20px rgba(0,0,0,0.5)",
    textAlign: "center",
  },
  title: {
    color: "#fff",
    marginBottom: "20px",
  },
  input: {
    width: "100%",
    padding: "10px",
    marginBottom: "15px",
    borderRadius: "5px",
    border: "1px solid #374151",
    background: "#1f2937",
    color: "#fff",
    outline: "none",
  },
  button: {
    width: "100%",
    padding: "10px",
    background: "#22c55e",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  link: {
    marginTop: "15px",
    color: "#3b82f6",
    cursor: "pointer",
    fontSize: "14px",
  },
};

export default Signup;