import cv2
import mediapipe as mp
import numpy as np
import os

# Gesture name
gesture_name = "hello"

# Create folder
save_path = f"collected_data/{gesture_name}"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

sample_count = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = []

            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # Save when pressing S
            key = cv2.waitKey(1)

            if key == ord('s'):
                np.save(
                    f"{save_path}/{sample_count}.npy",
                    np.array(landmarks)
                )

                print(f"Saved sample {sample_count}")

                sample_count += 1

    cv2.imshow("Collect Data", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()