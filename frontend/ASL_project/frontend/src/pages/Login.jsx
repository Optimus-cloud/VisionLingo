import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FcGoogle } from "react-icons/fc";
import { FaFacebook, FaLinkedin, FaGithub } from "react-icons/fa";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const navigate = useNavigate();

  const handleLogin = () => {
    if (email && password) {
      localStorage.setItem("user", email);
      navigate("/home");
    } else {
      alert("Enter credentials");
    }
  };

  return (
  <div style={styles.container}>
    <div style={styles.card}>
      <h1 style={styles.title}>Log in</h1>

      <p style={styles.sub}>
        New user?{" "}
        <span
          onClick={() => navigate("/signup")}
          style={styles.link}
        >
          Register Now
        </span>
      </p>

      <button style={styles.googleBtn}>
        <FcGoogle size={20} />
        Continue with Google
      </button>

      <div style={styles.icons}>
        <FaFacebook />
        <FaLinkedin />
        <FaGithub />
      </div>

      <div style={styles.divider}>
        <hr style={styles.hr} />
        <span>or</span>
        <hr style={styles.hr} />
      </div>

      <label style={styles.label}>
        Username or Email
      </label>

      <input
        style={styles.input}
        placeholder="Username or Email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <label style={styles.label}>
        Password
      </label>

      <div style={styles.passwordBox}>
        <input
          type={show ? "text" : "password"}
          style={styles.input}
          placeholder="Enter password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <span
          onClick={() => setShow(!show)}
          style={styles.eye}
        >
          {show ? (
            <AiOutlineEyeInvisible />
          ) : (
            <AiOutlineEye />
          )}
        </span>
      </div>

      <div style={styles.options}>
        <label style={{ color: "#FFFFFF" }}>
          <input type="checkbox" /> Remember Me
        </label>

        <span style={styles.link}>
          Forgot password
        </span>
      </div>

      <button
        style={styles.button}
        onClick={handleLogin}
      >
        Sign In
      </button>

      <p style={styles.footer}>
        By creating this account, you agree to
        our Privacy Policy
      </p>
    </div>
  </div>
);
}


const styles = {
  container: {
  width: "100%",
  minHeight: "100vh",

  display: "flex",
  justifyContent: "center",
  alignItems: "center",

  backgroundImage:
    "linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.25)), url('https://i.ibb.co/MkRJtwHj/image.png')",

  backgroundSize: "cover",
  backgroundPosition: "center",
  backgroundRepeat: "no-repeat",

  fontFamily: "Poppins, sans-serif",
},

  card: {
  background: "rgba(18, 7, 31, 0.95)",
  padding: "40px 30px",
  borderRadius: "20px",
  width: "380px",
  color: "#FFFFFF",
  border: "1px solid #8B5CF6",
  boxShadow: "0 0 30px rgba(139,92,246,0.35)",
},

  title: {
    fontSize: "32px",
    marginBottom: "5px",
    textAlign: "center",
    color: "#A855F7",
  },

  sub: {
    fontSize: "14px",
    textAlign: "center",
    marginBottom: "20px",
    color: "#D1D5DB",
  },

  link: {
    color: "#7C3AED",
    cursor: "pointer",
    fontWeight: "500",
  },

googleBtn: {
  width: "100%",
  padding: "12px",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  gap: "10px",
  border: "none",
  background: "#8B5CF6",
  color: "#000000",
  fontWeight: "600",
  marginBottom: "20px",
  borderRadius: "10px",
  cursor: "pointer",
},

  icons: {
    display: "flex",
    justifyContent: "center",
    gap: "20px",
    marginBottom: "20px",
    fontSize: "18px",
    color: "#71717a",
  },

  divider: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    marginBottom: "20px",
    color: "#71717a",
  },

  hr: {
    flex: 1,
    border: "0.5px solid #3f3f46",
  },

  label: {
    fontSize: "13px",
    marginBottom: "5px",
    display: "block",
    color: "#FFFFFF",
  },

  input: {
  width: "100%",
  padding: "12px",
  borderRadius: "10px",
  border: "1px solid #8B5CF6",
  backgroundImage:
  "linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), url('https://i.ibb.co/MkRJtwHj/image.png')",

backgroundSize: "cover",
backgroundPosition: "center",
backgroundRepeat: "no-repeat",
  color: "#FFFFFF",
  outline: "none",
  marginBottom: "12px",
  fontSize: "15px",
  WebkitBoxShadow: "0 0 0 1000px #000000 inset" ,
},

  passwordBox: {
    position: "relative",
    marginBottom: "15px",
  },

  eye: {
    position: "absolute",
    right: "12px",
    top: "50%",
    transform: "translateY(-50%)",
    cursor: "pointer",
    color: "#71717a",
  },

  options: {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  fontSize: "14px",
  marginBottom: "20px",
  color: "#FFFFFF",
},

  button: {
  width: "100%",
  padding: "13px",
  background:
    "linear-gradient(90deg,#7C3AED,#8B5CF6,#A855F7)",
  border: "none",
  color: "#FFFFFF",
  borderRadius: "10px",
  cursor: "pointer",
  fontWeight: "700",
  fontSize: "16px",
},
  footer: {
  fontSize: "11px",
  marginTop: "15px",
  color: "#D1D5DB",
  textAlign: "center",
},
}

export default Login; 