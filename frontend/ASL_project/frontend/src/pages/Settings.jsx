import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Settings() {
  const navigate = useNavigate();

  const [theme, setTheme] = useState(
    localStorage.getItem("theme") || "dark"
  );

  const currentTheme = theme;

  const themeColors = {
  background:
    currentTheme === "light"
      ? "#F8FAFC"
      : "#000000",

  card:
    currentTheme === "light"
      ? "#FFFFFF"
      : "#111111",

  text:
    currentTheme === "light"
      ? "#0F172A"
      : "#FFFFFF",

  subText:
    currentTheme === "light"
      ? "#475569"
      : "#D1D5DB",

  border:
    currentTheme === "light"
      ? "#E2E8F0"
      : "#222222",

  input:
    currentTheme === "light"
      ? "#F1F5F9"
      : "#000000",
};

  const [language, setLanguage] = useState(
    localStorage.getItem("language") || "English"
  );

  

  const [newUsername, setNewUsername] = useState("");

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  useEffect(() => {
    localStorage.setItem("theme", theme);
    localStorage.setItem("language", language);
  }, [theme, language]);

  const changeUsername = () => {
    const lastChange = localStorage.getItem("usernameChangeDate");

    if (lastChange) {
      const diff =
        (Date.now() - Number(lastChange)) /
        (1000 * 60 * 60 * 24);

      if (diff < 30) {
        alert(
          "Username can only be changed once every 30 days."
        );
        return;
      }
    }

    localStorage.setItem("username", newUsername);
    localStorage.setItem(
      "usernameChangeDate",
      Date.now()
    );

    
    alert("Username updated successfully");
  };

  const changePassword = () => {
    if (newPassword !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    alert(
      "Password update will work after backend integration."
    );
  };

  const forgotPassword = () => {
    alert(
      "Reset link will be sent after backend email integration."
    );
  };

    return (
  <div
    style={{
      display: "flex",
      minHeight: "100vh",
      background: themeColors.background,
      color: themeColors.text,
    }}
  >

    {/* SIDEBAR */}

<div style={styles.sidebar}>
  <h2 style={styles.logo}>
    🖐 Assamese Sign AI
  </h2>

  <div style={styles.menu}>
    <button
      style={styles.menuBtn}
      onClick={() => navigate("/home")}
    >
      🏠 Home
    </button>

    

    <button
  style={styles.menuBtn}
  onClick={() => navigate("/history")}
>
  📜 History
</button>

    <button style={styles.menuBtn}>
      💾 Saved Text
    </button>

    <button
  style={{
    ...styles.menuBtn,
    ...styles.activeMenu,
  }}
>
  ⚙ Settings
</button>
  </div>
</div>

<div
  style={{
    flex: 1,
    padding: "30px",
  }}
>

<h1
  style={{
    color: themeColors.text,
    marginBottom: "25px",
  }}
>
  ⚙ Settings
</h1>

      {/* Theme */}
<div
  style={{
    ...styles.card,
    background: themeColors.card,
    color: themeColors.text,
    border: themeColors.border,
  }}
>
  <h2
  style={{
    color: themeColors.text,
    fontSize: "32px",
    fontWeight: "700",
    marginBottom: "10px",
  }}
>
  Theme Settings
</h2>

  <p
  style={{
    color: themeColors.subText,
    fontSize: "18px",
  }}
>
  Choose Application Theme
</p>

  <select
    style={styles.input}
    value={theme}
    onChange={(e) =>
      setTheme(e.target.value)
    }
  >
    <option value="dark">
      🌙 Dark Theme
    </option>

    <option value="light">
      ☀ Light Theme
    </option>

  </select>
</div>

      

      {/* Language */}
<div
  style={{
    ...styles.card,
    background: themeColors.card,
    color: themeColors.text,
    border: themeColors.border,
  }}
>
        <h2
  style={{
    color:
      currentTheme === "light"
        ? "#0f172A"
        : "#FFFFFF",
    fontSize: "32px",
    fontWeight: "700",
    marginBottom: "10px",
  }}
>
  Language
</h2>

        <select
          value={language}
          onChange={(e) =>
            setLanguage(e.target.value)
          }
          style={styles.input}
        >
          <option>English</option>
          <option>Hindi</option>
          <option>Assamese</option>
          <option>Bengali</option>
          <option>French</option>
          <option>Spanish</option>
          <option>German</option>
          <option>Japanese</option>
        </select>
      </div>

      {/* Username */}
      <div
  style={{
    ...styles.card,
    background: themeColors.card,
    color: themeColors.text,
    border: themeColors.border,
  }}
>
        <h2
  style={{
    color:
      currentTheme === "light"
        ? "#0f172a"
        : "#ffffff",
    fontSize: "32px",
    fontWeight: "700",
    marginBottom: "10px",
  }}
>
  Username
</h2>

        

        <input
  style={{
    ...styles.input,
    background: "#000000",
    color: "#FFFFFF",
  }}
  placeholder="New Username"
  value={newUsername}
  onChange={(e) =>
    setNewUsername(e.target.value)
  }
/>

        <button
          style={styles.btn}
          onClick={changeUsername}
        >
          Update Username
        </button>
      </div>

      {/* Password */}
      <div
  style={{
    ...styles.card,
    background: themeColors.card,
    color: themeColors.text,
    border: themeColors.border,
  }}
>
        <h2
  style={{
    color:
      currentTheme === "light"
        ? "#0f172a"
        : "#ffffff",
    fontSize: "32px",
    fontWeight: "700",
    marginBottom: "10px",
  }}
>
  Change Password
</h2>

        <input
  style={{
    ...styles.input,
    background: "#000000",
    color: "#FFFFFF",
  }}
  type="password"
  placeholder="Current Password"
  value={currentPassword}
  onChange={(e) =>
    setCurrentPassword(e.target.value)
  }
/>

        <input
  style={{
    ...styles.input,
    background: "#000000",
    color: "#FFFFFF",
  }}
  type="password"
  placeholder="New Password"
  value={newPassword}
  onChange={(e) =>
    setNewPassword(e.target.value)
  }
/>

        <input
  style={{
    ...styles.input,
    background: "#000000",
    color: "#FFFFFF",
  }}
  type="password"
  placeholder="Confirm Password"
  value={confirmPassword}
  onChange={(e) =>
    setConfirmPassword(e.target.value)
  }
/>

        <button
          style={styles.btn}
          onClick={changePassword}
        >
          Change Password
        </button>

        <button
          style={styles.forgot}
          onClick={forgotPassword}
        >
          Forgot Password?
        </button>
      </div>

      <button
  style={styles.back}
  onClick={() =>
    navigate("/home")
  }
>
  Back to Home
</button>

</div>
</div>

);
}


const styles = {
  container: {
    minHeight: "100vh",
    padding: "30px",
    background:
      "linear-gradient(135deg,#0f0c29,#302b63,#24243e)",
    color: "white",
    fontFamily: "Poppins",
  },

  sidebar: {
  width: "280px",
  background: "#000000",
  padding: "30px",
  borderRight: "1px solid #222",
},

logo: {
  color: "#A855F7",
  marginBottom: "40px",
},

menu: {
  display: "flex",
  flexDirection: "column",
  gap: "15px",
},

menuBtn: {
  background: "transparent",
  color: "#FFFFFF",
  border: "none",
  padding: "14px",
  borderRadius: "12px",
  textAlign: "left",
  cursor: "pointer",
  fontSize: "16px",
},

activeMenu: {
  background: "#7C3AED",
  color: "#FFFFFF",
  fontWeight: "600",
  boxShadow: "0 0 15px rgba(168,85,247,0.4)",
},

  card: {
  padding: "30px",
  marginBottom: "25px",
  borderRadius: "20px",
  boxShadow: "0 8px 25px rgba(0,0,0,0.4)",
},

  input: {
  width: "100%",
  padding: "14px",
  marginBottom: "15px",
  borderRadius: "12px",
  border: "1px solid #333333",
  backgroundColor: "#000000",
  color: "#FFFFFF",
  fontSize: "16px",
  WebkitTextFillColor: "#FFFFFF",
},

  btn: {
  background: "linear-gradient(135deg,#7C3AED,#A855F7)",
  color: "#FFFFFF",
  border: "none",
  padding: "12px 18px",
  borderRadius: "10px",
  cursor: "pointer",
  fontWeight: "600",
},

  forgot: {
    marginLeft: "10px",
    background: "transparent",
    border: "none",
    color: "#facc15",
    cursor: "pointer",
  },

  back: {
  background: "linear-gradient(135deg,#7C3AED,#A855F7)",
  color: "#FFFFFF",
  border: "none",
  padding: "12px 20px",
  borderRadius: "10px",
  cursor: "pointer",
  fontWeight: "600",
},
};

export default Settings;