import os
import numpy as np

# Configurations
DATASET_PATH = "archive/keypoint.csv"
EXTENDED_DATASET_PATH = "archive/extended_keypoint.csv"
MODELS_DIR = "models"
SEQUENCE_LENGTH = 15  # Number of frames in a sequence for LSTM
NUM_FEATURES = 42      # 21 landmarks * 2 coordinates (x, y)

# Ensure models directory exists
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def normalize_landmarks(hand_landmarks, width=640, height=480):
    """
    Extracts x, y coordinates from MediaPipe hand landmarks,
    converts them to pixel coordinates, center-crops non-4:3 frames to a 4:3 
    aspect ratio to match the training data aspect ratio, translates the origin 
    to the wrist (landmark 0), and scales them by the maximum absolute coordinate value.
    
    Returns:
        List of 42 normalized coordinates: [x0, y0, x1, y1, ..., x20, y20]
    """
    actual_aspect_ratio = width / height
    target_aspect_ratio = 4.0 / 3.0
    
    raw_coords = []
    for lm in hand_landmarks.landmark:
        x_pixel = lm.x * width
        y_pixel = lm.y * height
        
        if actual_aspect_ratio > target_aspect_ratio:
            # Wider than 4:3 (e.g. 16:9). Crop sides.
            target_width = height * target_aspect_ratio
            excess_width = width - target_width
            x_cropped = x_pixel - (excess_width / 2.0)
            raw_coords.append((x_cropped, y_pixel))
        elif actual_aspect_ratio < target_aspect_ratio:
            # Taller than 4:3. Crop top/bottom.
            target_height = width / target_aspect_ratio
            excess_height = height - target_height
            y_cropped = y_pixel - (excess_height / 2.0)
            raw_coords.append((x_pixel, y_cropped))
        else:
            raw_coords.append((x_pixel, y_pixel))
        
    # 1. Wrist translation (wrist is landmark 0)
    wrist_x, wrist_y = raw_coords[0]
    rel_coords = []
    for x, y in raw_coords:
        rel_coords.append(x - wrist_x)
        rel_coords.append(y - wrist_y)
        
    # 2. Scaling by maximum absolute value
    max_val = max(abs(val) for val in rel_coords)
    if max_val == 0:
        # Avoid division by zero
        return rel_coords
        
    scaled_coords = [val / max_val for val in rel_coords]
    return scaled_coords
