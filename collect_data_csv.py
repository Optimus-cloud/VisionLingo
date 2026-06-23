import cv2
import mediapipe as mp
import numpy as np
import os
import csv

import utils

def main():
    # Ask for gesture label
    while True:
        try:
            label_input = input("Enter gesture label integer (e.g., 1 to 14, or any class ID): ").strip()
            label = int(label_input)
            break
        except ValueError:
            print("Please enter a valid integer.")

    print(f"\n--- Data Collection for Label: {label} ---")
    print("Instructions:")
    print("  - Press 's' to save a single frame's landmarks.")
    print("  - Press 'r' to toggle continuous recording (saves every frame where a hand is detected).")
    print("  - Press 'q' to quit.")
    print("------------------------------------------\n")

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

    # Ensure dataset directory exists
    dataset_dir = os.path.dirname(utils.DATASET_PATH)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    session_count = 0
    recording = False

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

        landmarks_to_save = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Normalize landmarks (using actual frame width and height)
                try:
                    landmarks_to_save = utils.normalize_landmarks(hand_landmarks, width=w, height=h)
                except Exception as e:
                    print(f"Error normalizing: {e}")

        # UI overlays
        status_text = "Recording: ON" if recording else "Recording: OFF"
        color = (0, 0, 255) if recording else (0, 255, 0)
        cv2.putText(frame, f"Label: {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, status_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, f"Saved: {session_count}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "S: Save, R: Rec, Q: Quit", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("VisionLingo Data Collection", frame)

        key = cv2.waitKey(1) & 0xFF

        # Handle keyboard inputs
        if key == ord('q'):
            break
        elif key == ord('s'):
            if landmarks_to_save is not None:
                # Save to CSV
                with open(utils.DATASET_PATH, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([label] + landmarks_to_save)
                session_count += 1
                print(f"Saved sample {session_count} to {utils.DATASET_PATH}")
            else:
                print("No hand detected in frame. Cannot save.")
        elif key == ord('r'):
            recording = not recording
            print(f"Continuous recording {'enabled' if recording else 'disabled'}.")

        # If recording is ON and we have landmarks, save automatically
        if recording and landmarks_to_save is not None:
            with open(utils.DATASET_PATH, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([label] + landmarks_to_save)
            session_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nSession finished. Added {session_count} samples to {utils.DATASET_PATH}")

if __name__ == "__main__":
    main()
