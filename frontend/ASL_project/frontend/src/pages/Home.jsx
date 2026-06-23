import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

/* =========================
   THEMES
========================= */

const themes = {
  light: {
  background: "#F1F5F9",
  sidebar: "#FFFFFF",
  card: "#FFFFFF",
  text: "#0F172A",
  subText: "#475569",
  border: "#CBD5E1",
  accent: "#7C3AED",
  input: "#E2E8F0",
},

  dark: {
  background: "#000000",
  sidebar: "#050505",
  card: "rgba(17,17,17,0.92)",
  text: "#FFFFFF",
  subText: "#D1D5DB",
  border: "#222222",
  accent: "#8B5CF6",
  input: "#1A1A1A",
},
};

function Home() {
  /* =========================
     REFS
  ========================= */

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  /* =========================
     THEME
  ========================= */

  const [theme] = useState(
    localStorage.getItem("theme") || "dark"
  );

  const currentTheme =
    themes[theme] || themes.dark;

  /* =========================
     STATES
  ========================= */

  const [activeTab, setActiveTab] =
  useState("home");

  const [prediction, setPrediction] =
    useState("Waiting...");

  const [sentence, setSentence] =
    useState("");

  const [history, setHistory] =
    useState([]);

  const [generatedText, setGeneratedText] =
    useState("");

  const [language, setLanguage] =
    useState("en");

  const [cameraStatus, setCameraStatus] =
    useState("Inactive");

  const [modelStatus] =
    useState("Connected");

  const [confidence] =
    useState("95%");

  const navigate = useNavigate();


  /* =========================
     AUTH CHECK
  ========================= */

  useEffect(() => {
    if (!localStorage.getItem("user")) {
      window.location.href = "/";
      return;
    }

    startCamera();
  }, []);

  /* =========================
     AUTO PREDICTION
  ========================= */

  useEffect(() => {
    const interval = setInterval(() => {
      captureFrame();
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  /* =========================
     START CAMERA
  ========================= */

  const startCamera = async () => {
    try {
      const stream =
        await navigator.mediaDevices.getUserMedia({
          video: true,
        });

      if (videoRef.current) {
        videoRef.current.srcObject =
          stream;

        setCameraStatus("Active");
      }
    } catch (error) {
      console.error(error);

      setCameraStatus("Error");
    }
  };

  /* =========================
     CAPTURE FRAME
  ========================= */

  const captureFrame = async () => {
    try {
      const canvas =
        canvasRef.current;

      const video =
        videoRef.current;

      if (!canvas || !video) return;

      canvas.width =
        video.videoWidth;

      canvas.height =
        video.videoHeight;

      const ctx =
        canvas.getContext("2d");

      ctx.drawImage(
        video,
        0,
        0
      );

      const image =
        canvas.toDataURL(
          "image/png"
        );

      const response =
        await axios.post(
          "http://localhost:5000/predict",
          {
            image,
          }
        );

      const newPrediction =
        response.data.prediction;

      setPrediction(
        newPrediction
      );

      setHistory((prev) => [
        ...prev.slice(-5),
        newPrediction,
      ]);
    } catch (error) {
      console.error(
        "Prediction Error:",
        error
      );
    }
  };

  /* =========================
     GENERATE OUTPUT
  ========================= */

  const generateOutput =
    async () => {
      try {
        const response =
          await axios.post(
            "https://libretranslate.de/translate",
            {
              q: sentence,
              source: "as",
              target: language,
              format: "text",
            }
          );

        setGeneratedText(
          response.data.translatedText
        );
      } catch (error) {
        console.error(error);
      }
    };

  /* =========================
     BUTTONS
  ========================= */

  const addLetter = () => {
    if (
      prediction &&
      prediction !== "Waiting..."
    ) {
      setSentence(
        (prev) =>
          prev + prediction
      );
    }
  };

  const clearText = () => {
    setSentence("");
    setGeneratedText("");
  };

  const saveText = () => {
    localStorage.setItem(
      "savedText",
      sentence
    );

    alert(
      "Text Saved Successfully"
    );
  };

  const logout = () => {
    localStorage.removeItem(
      "user"
    );

    window.location.href =
      "/";
  };

  return (
  <div
  style={{
    ...styles.container,

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
    {/* SIDEBAR */}

    <div
      style={{
        ...styles.sidebar,
        background:
          currentTheme.sidebar,
      }}
    >
      <h2
  style={{
    ...styles.logo,
    color:
      theme === "light"
        ? "#7C3AED"
        : "#8B5CF6",
  }}
>
        🖐 Assamese Sign AI
      </h2>

      <div style={styles.menu}>
        <button
  style={{
    ...styles.menuBtn,
    ...styles.activeMenu,
  }}
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
  style={styles.menuBtn}
  onClick={() =>
    (window.location.href = "/settings")
  }
>
  ⚙ Settings
</button>
        
      </div>

      <button
        style={styles.logoutBtn}
        onClick={logout}
      >
        Logout
      </button>
    </div>

    {/* MAIN CONTENT */}

    <div style={styles.main}>
      <h1
        style={{
          ...styles.title,
          color:
            currentTheme.text,
        }}
      >
        Assamese Sign Language
         System
      </h1>

      {/* TOP SECTION */}

      <div style={styles.topGrid}>
        {/* CAMERA */}

        <div
          style={{
            ...styles.card,
            background:
              currentTheme.card,
          }}
        >
          <h3>
            📷 Live Camera Feed
          </h3>

          <video
            ref={videoRef}
            autoPlay
            style={styles.video}
          />

          <canvas
            ref={canvasRef}
            style={{
              display: "none",
            }}
          />
        </div>

        {/* RIGHT PANEL */}

        <div style={styles.rightPanel}>
          {/* DETECTED SIGN */}

          <div
            style={{
              ...styles.card,
              background:
                currentTheme.card,
            }}
          >
            <h3>
              Detected Sign
            </h3>

            <h1
              style={
                styles.signText
              }
            >
              {prediction}
            </h1>
          </div>

          {/* CONFIDENCE */}

          <div
            style={{
              ...styles.card,
              background:
                currentTheme.card,
            }}
          >
            <h3>
              Confidence
            </h3>

            <h2
  style={{
    color: currentTheme.text,
  }}
>
  {confidence}
</h2>
          </div>

          {/* STATUS */}

          <div
            style={{
              ...styles.card,
              background:
                currentTheme.card,
            }}
          >
            <p>
              📷 Camera:
              {" "}
              {cameraStatus}
            </p>

            <p>
              🤖 Model:
              {" "}
              {modelStatus}
            </p>
          </div>
        </div>
      </div>

      {/* ASSAMESE TEXT */}

      <div
        style={{
          ...styles.card,
          background:
            currentTheme.card,
        }}
      >
        <h2
  style={{
    color: currentTheme.text,
  }}
>
  Recognized Assamese Text
</h2>

        <p
  style={{
    ...styles.textArea,
    color:
      theme === "dark"
        ? "#FFFFFF"
        : "#0F172A",
  }}
>
  {sentence || "Waiting for gestures..."}
</p>

        <div
          style={styles.buttonRow}
        >
          <button
            style={
              styles.addBtn
            }
            onClick={
              addLetter
            }
          >
            Add Letter
          </button>

          <button
            style={
              styles.clearBtn
            }
            onClick={
              clearText
            }
          >
            Clear
          </button>

          <button
            style={
              styles.saveBtn
            }
            onClick={
              saveText
            }
          >
            Save
          </button>
        </div>
      </div>

      {/* OUTPUT SECTION */}

      <div
        style={{
          ...styles.card,
          background:
            currentTheme.card,
        }}
      >
        <h2
  style={{
    color: currentTheme.text,
  }}
>
  Generate Output
</h2>

        <div
          style={styles.outputRow}
        >
          <select
            style={
              styles.select
            }
            value={language}
            onChange={(e) =>
              setLanguage(
                e.target.value
              )
            }
          >
            <option value="en">
              English
            </option>

            <option value="hi">
              Hindi
            </option>

            <option value="bn">
              Bengali
            </option>

            <option value="fr">
              French
            </option>

            <option value="de">
              German
            </option>

            <option value="ja">
              Japanese
            </option>

            <option value="ar">
              Arabic
            </option>
          </select>

          <button
            style={
              styles.generateBtn
            }
            onClick={
              generateOutput
            }
          >
            Generate
          </button>
        </div>

        <div
          style={
            styles.generatedBox
          }
        >
          {generatedText ||
            "Output will appear here"}
        </div>
      </div>

      {/* RECENT SIGNS */}

      <div
        style={{
          ...styles.card,
          background:
            currentTheme.card,
        }}
      >
        <h2>
          Recent Predictions
        </h2>

        <div
          style={
            styles.historyGrid
          }
        >
          {history.length === 0 ? (
  <p>No History Available</p>
) : (
  history.map((item, index) => (
    <div
      key={index}
      style={styles.historyCard}
    >
      {item}
    </div>
  ))
)}
        </div>
      </div>
    </div>
  </div>
);
}

const styles = {
  container: {
    display: "flex",
    minHeight: "100vh",
    fontFamily: "Poppins, sans-serif",
  },

  /* SIDEBAR */

  sidebar: {
    width: "250px",
    padding: "25px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between", 
    boxShadow:
  "4px 0 15px rgba(0,0,0,0.08)",
    borderRight: "1px solid #222222",
  },

  

  menu: {
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },

menuBtn: {
  background: "transparent",
  color: "inherit",
  border: "none",
  padding: "14px 16px",
  textAlign: "left",
  cursor: "pointer",
  fontSize: "16px",
  borderRadius: "12px",
  transition: "0.3s",
},

  activeMenu: {
  background:
    "linear-gradient(135deg,#7C3AED,#A855F7)",
  color: "#ffffff",
  fontWeight: "600",
},

  logoutBtn: {
    background: "#ef4444",
    color: "white",
    border: "none",
    padding: "12px",
    borderRadius: "10px",
    cursor: "pointer",
    fontWeight: "600",
  },

  /* MAIN */

  main: {
    flex: 1,
    padding: "25px",
  },

  title: {
    marginBottom: "25px",
    fontSize: "32px",
    fontWeight: "700",
  },

  /* GRID */

  topGrid: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "20px",
    marginBottom: "20px",
  },

  rightPanel: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },

  /* CARDS */

  card: {
  padding: "20px",
  borderRadius: "18px",
  border: "1px solid #222222",
  boxShadow:
    "0 10px 30px rgba(0,0,0,0.45)",
},

  /* CAMERA */

  video: {
    width: "100%",
    borderRadius: "12px",
    background: "black",
  },

  /* DETECTED SIGN */

  signText: {
    fontSize: "60px",
    fontWeight: "700",
    textAlign: "center",
    color: "#f97316",
    marginTop: "10px",
  },

  /* ASSAMESE TEXT */

  textArea: {
  minHeight: "80px",
  fontSize: "22px",
  marginTop: "15px",
  padding: "15px",
  borderRadius: "12px",
  background: "rgba(255,255,255,0.05)",
  color: "#000000",
  fontWeight: "600",
},

  buttonRow: {
    display: "flex",
    gap: "12px",
    marginTop: "15px",
  },

  addBtn: {
  background: "#8B5CF6",
  color: "#000000",
  border: "none",
  padding: "12px 18px",
  borderRadius: "10px",
  cursor: "pointer",
  fontWeight: "600",
  fontFamily: "Poppins, sans-serif",
fontSize: "16px",
fontWeight: "600",
color: "black",
},

  clearBtn: {
  background: "#8B5CF6",
  color: "#000000",
  border: "none",
  padding: "12px 18px",
  borderRadius: "10px",
  cursor: "pointer",
  fontFamily: "Poppins, sans-serif",
fontSize: "16px",
fontWeight: "600",
color: "black",
},

  saveBtn: {
  background: "#8B5CF6",
  color: "#000000",
  border: "none",
  padding: "12px 18px",
  borderRadius: "10px",
  cursor: "pointer",
  fontFamily: "Poppins, sans-serif",
fontSize: "16px",
fontWeight: "600",
color: "black",
},

  /* OUTPUT */

  outputRow: {
    display: "flex",
    gap: "12px",
    marginBottom: "15px",
  },

  select: {
    padding: "12px",
    borderRadius: "10px",
    border: "none",
    minWidth: "180px",
  },

  generateBtn: {
  background: "#8B5CF6",
  color: "#000000",
  border: "none",
  padding: "12px 18px",
  borderRadius: "10px",
  cursor: "pointer",
  fontWeight: "600",
  fontFamily: "Poppins, sans-serif",
fontSize: "16px",
color: "black",
},

  generatedBox: {
    minHeight: "80px",
    padding: "15px",
    borderRadius: "12px",
    background:
      "rgba(255,255,255,0.05)",
    fontSize: "20px",
  },

  /* HISTORY */

  historyGrid: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
    marginTop: "15px",
  },

  historyCard: {
    padding: "15px 20px",
    borderRadius: "12px",
    background: "#8b5cf6",
    color: "white",
    fontWeight: "600",
  },
};
export default Home;