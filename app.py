import os
import base64
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mediapipe as mp

import utils

app = Flask(__name__)
CORS(app)

# Load trained models on startup
print("Loading trained models for Web API server...")
try:
    fnn_model = tf.keras.models.load_model(os.path.join(utils.MODELS_DIR, "fnn_model.keras"))
    fnn_classes = np.load(os.path.join(utils.MODELS_DIR, "fnn_classes.npy"))
    print("FNN model loaded successfully.")
except Exception as e:
    fnn_model, fnn_classes = None, None
    print(f"Warning: Could not load FNN model. Run 'train_fnn.py' first. Error: {e}")

try:
    lstm_model = tf.keras.models.load_model(os.path.join(utils.MODELS_DIR, "lstm_model.keras"))
    lstm_classes = np.load(os.path.join(utils.MODELS_DIR, "lstm_classes.npy"))
    print("LSTM model loaded successfully.")
except Exception as e:
    lstm_model, lstm_classes = None, None
    print(f"Warning: Could not load LSTM model. Run 'train_lstm.py' first. Error: {e}")

# Initialize MediaPipe Hands on server-side (for backward compatibility)
mp_hands = mp.solutions.hands
hands_api = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.5
)

# Custom mappings (aligned with your custom gesture database)
ASSAMESE_MAP = {
    "1": "O",
    "2": "I",
    "3": "I",
    "4": "U",
    "5": "O",
    "6": "K",
    "7": "E",
    "8": "J",
    "9": "L"
}

WORD_TRANSLATION_MAP = {
    "KL": "Banana / Tap (Kol)",
    "JL": "Water (Jol)",
    "EK": "One (Ek)",
    "OL": "Few / Little (Ol)",
    "KOL": "Banana / Tap (Kol)",
    "JOL": "Water (Jol)",
    "LOK": "People (Lok)",
    "KUL": "Jujube Fruit / Clan (Kul)",
    "KIL": "Fist Blow / Punch (Kil)",
    "JOK": "Leech (Jok)",
    "OI": "Hey / Listen (Oi)"
}

# Temporary database for user accounts
users = []

def decode_base64_image(base64_string):
    """Decodes a base64-encoded image string into an OpenCV BGR image."""
    try:
        if ',' in base64_string:
            parts = base64_string.split(',')
            if len(parts) > 1 and parts[1]:
                base64_string = parts[1]
            else:
                return None
        if not base64_string.strip():
            return None
            
        img_data = base64.b64decode(base64_string)
        nparr = np.frombuffer(img_data, np.uint8)
        if len(nparr) == 0:
            return None
            
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame
    except Exception:
        return None

# --- Home Route (Serves the new frontend) ---

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# --- Authentication Routes ---

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid signup data"}), 400
        
    email = data["email"]
    password = data["password"]

    # Check if user exists
    for user in users:
        if user["email"] == email:
            return jsonify({"message": "User already exists"}), 400

    users.append({"email": email, "password": password})
    return jsonify({"message": "Signup successful"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid login data"}), 400
        
    email = data["email"]
    password = data["password"]

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({"message": "Login success"}), 200

    return jsonify({"message": "Invalid credentials"}), 401


# --- Gesture Recognition Endpoint (Supports both images & coordinates) ---

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    if not data:
        return jsonify({"prediction": "No JSON body provided", "confidence": "0%"}), 400

    model_type = data.get("model", "fnn").lower()

    # 1. Direct coordinate array prediction (FNN: 42 coordinates)
    if "landmarks" in data and isinstance(data["landmarks"], list) and len(data["landmarks"]) == utils.NUM_FEATURES:
        if fnn_model is None:
            return jsonify({"prediction": "FNN model not loaded", "confidence": "0%"}), 503
        try:
            scaled_coords = data["landmarks"]
            input_data = np.expand_dims(scaled_coords, axis=0).astype(np.float32)
            predictions = fnn_model(input_data, training=False).numpy()[0]
            class_idx = np.argmax(predictions)
            pred_class = str(fnn_classes[class_idx])
            confidence = float(predictions[class_idx])
            letter = ASSAMESE_MAP.get(pred_class, pred_class)
            
            # Print debug information to the console
            print(f"[DEBUG] FNN - Min/Max Coords: {min(scaled_coords):.3f}/{max(scaled_coords):.3f} | Softmax Probabilities: {np.round(predictions, 3)} | Class: {pred_class} -> {letter} ({confidence * 100:.1f}%)")
            
            return jsonify({
                "prediction": letter,
                "confidence": f"{confidence * 100:.1f}%",
                "class": pred_class
            })
        except Exception as e:
            return jsonify({"prediction": f"FNN prediction failed: {str(e)}", "confidence": "0%"}), 500

    # 2. Direct sequence array prediction (LSTM: 15 frames of 42 coordinates)
    elif "sequence" in data and isinstance(data["sequence"], list) and len(data["sequence"]) == utils.SEQUENCE_LENGTH:
        if lstm_model is None:
            return jsonify({"prediction": "LSTM model not loaded", "confidence": "0%"}), 503
        try:
            sequence_normalized = data["sequence"]
            input_data = np.expand_dims(sequence_normalized, axis=0).astype(np.float32)
            predictions = lstm_model(input_data, training=False).numpy()[0]
            class_idx = np.argmax(predictions)
            pred_class = str(lstm_classes[class_idx])
            confidence = float(predictions[class_idx])
            letter = ASSAMESE_MAP.get(pred_class, pred_class)
            
            # Print debug information to the console
            print(f"[DEBUG] LSTM - Sequence Count: {len(sequence_normalized)} | Softmax Probabilities: {np.round(predictions, 3)} | Class: {pred_class} -> {letter} ({confidence * 100:.1f}%)")
            
            return jsonify({
                "prediction": letter,
                "confidence": f"{confidence * 100:.1f}%",
                "class": pred_class
            })
        except Exception as e:
            return jsonify({"prediction": f"LSTM prediction failed: {str(e)}", "confidence": "0%"}), 500

    # 3. Base64 Image prediction (for backward compatibility / image streams)
    elif "image" in data:
        if fnn_model is None:
            return jsonify({"prediction": "FNN model not loaded on server", "confidence": "0%"}), 503
        try:
            frame = decode_base64_image(data["image"])
            if frame is None or frame.size == 0 or frame.shape[0] == 0 or frame.shape[1] == 0:
                return jsonify({"prediction": "No camera feed", "confidence": "0%"})
                
            h, w, c = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands_api.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    scaled_coords = utils.normalize_landmarks(hand_landmarks, width=w, height=h)
                    input_data = np.expand_dims(scaled_coords, axis=0).astype(np.float32)

                    predictions = fnn_model(input_data, training=False).numpy()[0]
                    class_idx = np.argmax(predictions)
                    pred_class = str(fnn_classes[class_idx])
                    confidence = float(predictions[class_idx])
                    letter = ASSAMESE_MAP.get(pred_class, pred_class)

                    return jsonify({
                        "prediction": letter,
                        "confidence": f"{confidence * 100:.1f}%",
                        "class": pred_class
                    })

            return jsonify({
                "prediction": "No hand detected",
                "confidence": "0%"
            })
        except Exception as e:
            return jsonify({"prediction": f"Error: {str(e)}", "confidence": "0%"}), 500

    else:
        return jsonify({"prediction": "Invalid predict payload", "confidence": "0%"}), 400


@app.route("/translate", methods=["POST"])
def translate():
    """Translates an accumulated word spelling into its English meaning."""
    data = request.json
    if not data or "word" not in data:
        return jsonify({"error": "No word spelling provided"}), 400

    word = data["word"].strip().upper()
    translation = WORD_TRANSLATION_MAP.get(word, "Unknown Spelling")
    
    return jsonify({
        "word": word,
        "translation": translation
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

