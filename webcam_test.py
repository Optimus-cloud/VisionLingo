import cv2
import mediapipe as mp

try:
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,  # Faster processing
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # Drawing utility
    mp_draw = mp.solutions.drawing_utils

    # Open webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Reduce resolution for smooth performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to read webcam")
            break

        # Flip for mirror effect
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Improve performance
        rgb_frame.flags.writeable = False
        results = hands.process(rgb_frame)
        rgb_frame.flags.writeable = True

        # Draw landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        # Show webcam
        cv2.imshow("VisionLingo Webcam Test", frame)

        # Quit on Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print("Error:", e)
    input("Press Enter to close...")