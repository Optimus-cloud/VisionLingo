import { useNavigate } from "react-router-dom";

function History() {
  const navigate = useNavigate();

  const theme =
  localStorage.getItem("theme") || "dark";

  const themeColors = {
  background: theme === "light" ? "#F8FAFC" : "#000000",
  card: theme === "light" ? "#FFFFFF" : "#111111",
  text: theme === "light" ? "#000000" : "#FFFFFF",
  border: theme === "light" ? "#CBD5E1" : "#333333",
  sidebar: theme === "light" ? "#FFFFFF" : "#000000",
};

const currentTheme = {
  background:
    theme === "light"
      ? "#F8FAFC"
      : "#000000",

  sidebar:
    theme === "light"
      ? "#FFFFFF"
      : "#000000",

  card:
    theme === "light"
      ? "#FFFFFF"
      : "#111111",

  text:
    theme === "light"
      ? "#0F172A"
      : "#FFFFFF",

  border:
    theme === "light"
      ? "#CBD5E1"
      : "#333333",
};

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      
      {/* Sidebar */}
      <div
  style={{
    ...styles.sidebar,
    background: currentTheme.sidebar,
    borderRight: `1px solid ${currentTheme.border}`,
  }}
>
        <h2
  style={{
    ...styles.logo,
    color: "#A855F7",
  }}
>
          🖐 Assamese Sign AI
        </h2>

        <div style={styles.menu}>
          <button
  style={{
    ...styles.menuBtn,
    color: theme === "dark" ? "#FFFFFF" : "#000000",
  }}
  onClick={() => navigate("/home")}
>
  🏠 Home
</button>

          <button
            style={{
              ...styles.menuBtn,
              ...styles.activeMenu,
            }}
          >
            📜 History
          </button>

          <button
  style={{
    ...styles.menuBtn,
    color: theme === "dark" ? "#FFFFFF" : "#000000",
  }}
>
  💾 Saved Text
</button>

          <button
  style={{
    ...styles.menuBtn,
    color: theme === "dark" ? "#FFFFFF" : "#000000",
  }}
  onClick={() => navigate("/settings")}
>
  ⚙ Settings
</button>
        </div>
      </div>

      {/* Content */}
      <div
  style={{
    ...styles.content,

    background:
      theme === "dark"
        ? `linear-gradient(rgba(0,0,0,0.25), rgba(0,0,0,0.25)),
           url("https://i.ibb.co/MkRJtwHj/image.png")`
        : currentTheme.background,

    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",

    color: currentTheme.text,
  }}
>
        <h1 style={{ color: themeColors.text }}>
  📜 History
</h1>

        <div
  style={{
    ...styles.card,
    background:
      theme === "dark"
        ? "rgba(17,17,17,0.92)"
        : themeColors.card,

    color: themeColors.text,
    border: `1px solid ${themeColors.border}`,
  }}
>
          <h2 style={{ color: themeColors.text }}>
  No History Available
</h2>

          <p>
            Start using sign detection to generate history.
          </p>
        </div>
      </div>
    </div>
  );
}

const styles = {
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
  },

  content: {
  flex: 1,
  padding: "30px",
},

  card: {
  padding: "30px",
  borderRadius: "20px",
},
};

export default History;