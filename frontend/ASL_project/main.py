# main.py

import mediapipe as mp
import numpy as np
import pickle
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

labels_dict = {
    0: "অ",
    1: "আ",
    2: "ই"
}

model = pickle.load(open("model.p", "rb"))

def extract_landmarks(hand_landmarks):
    x_coords = [lm.x for lm in hand_landmarks.landmark]
    y_coords = [lm.y for lm in hand_landmarks.landmark]

    min_x = min(x_coords)
    min_y = min(y_coords)

    data = []
    for lm in hand_landmarks.landmark:
        data.append(lm.x - min_x)
        data.append(lm.y - min_y)

    return data


def predict_from_frame(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            temp = extract_landmarks(hand_landmarks)
            pred = model.predict([temp])[0]
            return labels_dict[pred]

    return "No hand detected"