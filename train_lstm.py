import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import utils

def train_lstm():
    # Force using the clean base dataset to avoid corrupted label overlaps
    dataset_file = utils.DATASET_PATH
    print(f"Using clean base dataset: {dataset_file}")

    if not os.path.exists(dataset_file):
        raise FileNotFoundError(f"Dataset file {dataset_file} not found. Please collect data first.")

    # 1. Load data
    print("Loading dataset...")
    df = pd.read_csv(dataset_file, header=None, on_bad_lines='skip')
    print(f"Dataset loaded. Shape: {df.shape}")

    # Column 0 is the label, columns 1 to 42 are features (x, y coordinates)
    y = df.iloc[:, 0].values
    X = df.iloc[:, 1:43].values

    # 2. Form sequences per class (Slide 12: Sequence Formation)
    print(f"Forming sequences of length {utils.SEQUENCE_LENGTH}...")
    X_seq = []
    y_seq = []

    unique_classes = np.unique(y)
    for cls in unique_classes:
        # Extract all samples belonging to this class
        cls_indices = np.where(y == cls)[0]
        cls_X = X[cls_indices]

        # Check if we have enough samples to form at least one sequence
        if len(cls_X) < utils.SEQUENCE_LENGTH:
            print(f"Warning: Class {cls} has only {len(cls_X)} samples. Skipping sequence formation for this class.")
            continue

        # Apply a sliding window of size SEQUENCE_LENGTH
        for i in range(len(cls_X) - utils.SEQUENCE_LENGTH + 1):
            window = cls_X[i : i + utils.SEQUENCE_LENGTH]
            X_seq.append(window)
            y_seq.append(cls)

    X_seq = np.array(X_seq)
    y_seq = np.array(y_seq)

    print(f"Formed {X_seq.shape[0]} sequences. X_seq shape: {X_seq.shape}")

    # 3. Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_seq)
    num_classes = len(label_encoder.classes_)
    print(f"Encoded labels for {num_classes} classes: {label_encoder.classes_}")

    # Save classes for real-time decoding
    np.save(os.path.join(utils.MODELS_DIR, "lstm_classes.npy"), label_encoder.classes_)
    print("Saved label encoder classes to models/lstm_classes.npy")

    # 4. Train-test split (75% train, 25% test as per Slide 17)
    X_train, X_test, y_train, y_test = train_test_split(
        X_seq, y_encoded, test_size=0.25, random_state=42, stratify=y_encoded
    )
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

    # 5. Build LSTM Model
    print("Building LSTM model...")
    model = Sequential([
        Input(shape=(utils.SEQUENCE_LENGTH, utils.NUM_FEATURES)),
        LSTM(64, return_sequences=True),
        Dropout(0.3),
        LSTM(64, return_sequences=False),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.summary()

    # 6. Callbacks: Early Stopping (Slide 13) and Model Checkpoint
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True, verbose=1),
        ModelCheckpoint(
            filepath=os.path.join(utils.MODELS_DIR, "lstm_model.keras"),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]

    # Calculate balanced class weights to eliminate bias towards classes with large sample sizes
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = dict(zip(np.unique(y_train), class_weights))
    print(f"Applying class weights: {class_weight_dict}")

    # 7. Train the model
    print("Training LSTM model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=120,
        batch_size=32,
        callbacks=callbacks,
        class_weight=class_weight_dict
    )

    # 8. Evaluate the model
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nFinal Test Accuracy: {test_acc:.4f}")
    print(f"Final Test Loss: {test_loss:.4f}")
    print("LSTM model training completed successfully and saved to models/lstm_model.keras")

if __name__ == "__main__":
    train_lstm()
