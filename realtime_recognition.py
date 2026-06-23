import cv2
import mediapipe as mp
import numpy as np
import os
import argparse
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont

import utils

# Mapping of labels to single English letters for spelling words
ASSAMESE_MAP = {
    "1": "O",
    "2": "I",
    "3": "I",
    "4": "U",
    "5": "O",
    "6": "K",
    "7": "E",
    "8": "J",
    "9": "L",
    "10": "X",
    "11": "Y",
    "12": "Z",
    "13": "A",
    "14": "B"
}

# Translates accumulated Assamese letters into English meanings
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

def draw_unicode_text(img, text, position, font_size=28, color=(255, 255, 255)):
    """
    Helper to draw Unicode text (like Assamese characters) on an OpenCV image
    using Pillow's TrueType font support.
    """
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # Try to load a system font that supports Indian scripts. 
    # On Windows, Arial or Segoe UI usually work well.
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("msgothic.ttc", font_size)
        except IOError:
            font = ImageFont.load_default()
            
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def main():
    parser = argparse.ArgumentParser(description="VisionLingo Real-Time Gesture Recognition")
    parser.add_argument(
        "--model",
        type=str,
        default="fnn",
        choices=["fnn", "lstm"],
        help="Model type to run (fnn or lstm)"
    )
    args = parser.parse_args()

    # Define paths
    if args.model == "fnn":
        model_path = os.path.join(utils.MODELS_DIR, "fnn_model.keras")
        classes_path = os.path.join(utils.MODELS_DIR, "fnn_classes.npy")
    else:
        model_path = os.path.join(utils.MODELS_DIR, "lstm_model.keras")
        classes_path = os.path.join(utils.MODELS_DIR, "lstm_classes.npy")

    # Check model files
    if not os.path.exists(model_path) or not os.path.exists(classes_path):
        print(f"Error: Model file or classes file not found at:")
        print(f"  Model: {model_path}")
        print(f"  Classes: {classes_path}")
        print(f"Please run the training script ('train_{args.model}.py') first.")
        return

    # Load Model and Class list
    print(f"Loading {args.model.upper()} model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    classes = np.load(classes_path)
    print(f"Model loaded successfully. Target classes: {classes}")

    # MediaPipe setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,  # Set to 1 for higher landmark accuracy
        min_detection_confidence=0.75,  # Increased to prevent ghost hands
        min_tracking_confidence=0.75   # Increased to prevent ghost hands
    )
    mp_draw = mp.solutions.drawing_utils

    # Webcam setup
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # State variables for gesture locking and accumulation
    sequence_buffer = []
    accumulated_letters = []
    
    hold_counter = 0
    last_predicted = None
    locked_gesture = None
    no_hand_counter = 0
    
    HOLD_THRESHOLD = 15       # Hold same gesture for 15 frames (~0.5 sec) to store/lock it
    COOLDOWN_THRESHOLD = 12   # No hand for 12 frames (~0.4 sec) to finalize and output the stored gesture

    print(f"\nStarting webcam for {args.model.upper()} inference.")
    print("Instructions:")
    print("  - Hold a hand gesture stably to see the green target class and start charging.")
    print("  - Once charged, the gesture becomes 'LOCKED' (yellow).")
    print("  - REMOVE your hand to 'output' the letter and append it to the word.")
    print("  - Press 'c' to clear the accumulated word.")
    print("  - Press 'q' to exit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read webcam.")
            break

        # Mirror effect
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = hands.process(rgb_frame)
        rgb_frame.flags.writeable = True

        current_prediction = None
        confidence = 0.0

        if results.multi_hand_landmarks:
            no_hand_counter = 0  # Reset hand removal timer
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw skeleton
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Normalize landmarks (using actual frame width and height)
                try:
                    scaled_coords = utils.normalize_landmarks(hand_landmarks, width=w, height=h)
                except Exception as e:
                    print(f"Error normalizing landmarks: {e}")
                    continue

                if args.model == "fnn":
                    # FNN expects input of shape (1, 42)
                    input_data = np.expand_dims(scaled_coords, axis=0).astype(np.float32)
                    predictions = model(input_data, training=False).numpy()[0]
                    class_idx = np.argmax(predictions)
                    current_prediction = str(classes[class_idx])
                    confidence = predictions[class_idx]
                
                elif args.model == "lstm":
                    # LSTM expects input of shape (1, sequence_length, 42)
                    sequence_buffer.append(scaled_coords)
                    if len(sequence_buffer) > utils.SEQUENCE_LENGTH:
                        sequence_buffer.pop(0)
                        
                    if len(sequence_buffer) == utils.SEQUENCE_LENGTH:
                        input_data = np.expand_dims(sequence_buffer, axis=0).astype(np.float32)
                        predictions = model(input_data, training=False).numpy()[0]
                        class_idx = np.argmax(predictions)
                        current_prediction = str(classes[class_idx])
                        confidence = predictions[class_idx]

            # Update holding state machine (lowered threshold to 0.45 for better sensitivity)
            if current_prediction is not None and confidence > 0.45:
                if current_prediction == last_predicted:
                    hold_counter += 1
                else:
                    last_predicted = current_prediction
                    hold_counter = 0
                
                # Lock the gesture if held long enough
                if hold_counter >= HOLD_THRESHOLD:
                    locked_gesture = current_prediction
            else:
                hold_counter = max(0, hold_counter - 1)
        else:
            # No hand detected
            sequence_buffer.clear()
            hold_counter = 0
            last_predicted = None
            no_hand_counter += 1
            
            # If hand was removed for enough frames, finalize the locked gesture
            if no_hand_counter >= COOLDOWN_THRESHOLD:
                if locked_gesture is not None:
                    char_repr = ASSAMESE_MAP.get(locked_gesture, f"Label {locked_gesture}")
                    accumulated_letters.append(char_repr)
                    print(f"\n[Added Letter]: {char_repr} (Class {locked_gesture})")
                    print(f"Current Word  : {''.join(accumulated_letters)}")
                    locked_gesture = None
                no_hand_counter = 0

        # UI Overlay - Dark semi-transparent box (extended height to 180)
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (450, 180), (20, 20, 20), -1)
        cv2.rectangle(overlay, (10, 10), (450, 180), (120, 120, 120), 2)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        # Build information texts
        model_name = args.model.upper()
        
        # Real-time state presentation
        if current_prediction is not None:
            char_preview = ASSAMESE_MAP.get(current_prediction, current_prediction)
            realtime_text = f"Current: {char_preview} (Class {current_prediction}) ({confidence:.1%})"
            
            # Progress bar for holding
            progress_pct = min(1.0, hold_counter / HOLD_THRESHOLD)
            bar_w = int(180 * progress_pct)
            cv2.rectangle(frame, (250, 50), (430, 60), (50, 50, 50), -1)
            cv2.rectangle(frame, (250, 50), (250 + bar_w, 60), (0, 255, 0), -1)
        else:
            realtime_text = "Current: None"

        if locked_gesture is not None:
            locked_char = ASSAMESE_MAP.get(locked_gesture, locked_gesture)
            lock_text = f"Locked Pose: {locked_char} (Class {locked_gesture}) (Remove hand to output)"
            lock_color = (0, 255, 255) # Yellow
        else:
            lock_text = "Locked Pose: None"
            lock_color = (200, 200, 200)

        word_formed = "".join(accumulated_letters)
        sentence_text = f"Word Formed: {word_formed}"
        
        # Word Translation Lookup
        if word_formed:
            translation = WORD_TRANSLATION_MAP.get(word_formed.upper(), "Spelling...")
        else:
            translation = "None"

        # Draw texts using helper for Unicode
        frame = draw_unicode_text(frame, f"Model: {model_name}", (20, 15), font_size=20, color=(255, 255, 255))
        frame = draw_unicode_text(frame, realtime_text, (20, 42), font_size=22, color=(0, 255, 0))
        frame = draw_unicode_text(frame, lock_text, (20, 75), font_size=20, color=lock_color)
        frame = draw_unicode_text(frame, sentence_text, (20, 108), font_size=22, color=(255, 150, 50))
        frame = draw_unicode_text(frame, f"Translation: {translation}", (20, 140), font_size=22, color=(0, 240, 255))

        # Bottom info bar
        cv2.putText(frame, "C: Clear Word | Q: Quit", (15, h - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("VisionLingo Real-Time Gesture Recognition", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            accumulated_letters.clear()
            print("Cleared accumulated word.")

    cap.release()
    cv2.destroyAllWindows()
    
    # Print the final translation summary beautifully in the terminal
    final_word = "".join(accumulated_letters)
    if final_word:
        final_translation = WORD_TRANSLATION_MAP.get(final_word.upper(), "Unknown Spelling")
    else:
        final_word = "[No letters spelled]"
        final_translation = "N/A"
        
    print("\n" + "="*50)
    print("   VISIONLINGO SIGN LANGUAGE TRANSLATION RESULT   ")
    print("="*50)
    print(f" Spelled Letters : {' '.join(accumulated_letters)}")
    print(f" Final Word      : {final_word}")
    print(f" Translation     : {final_translation}")
    print("="*50)
    print(" Thank you for using VisionLingo!\n")

if __name__ == "__main__":
    main()
