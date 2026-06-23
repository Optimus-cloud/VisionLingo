import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import utils

def train_fnn():
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

    # 2. Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    num_classes = len(label_encoder.classes_)
    print(f"Encoded labels for {num_classes} classes: {label_encoder.classes_}")

    # Save classes for real-time decoding
    np.save(os.path.join(utils.MODELS_DIR, "fnn_classes.npy"), label_encoder.classes_)
    print("Saved label encoder classes to models/fnn_classes.npy")

    # 3. Train-test split (75% train, 25% test as per Slide 17)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.25, random_state=42, stratify=y_encoded
    )
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

    # 4. Build FNN Model
    print("Building Feedforward Neural Network model...")
    model = Sequential([
        Input(shape=(utils.NUM_FEATURES,)),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        BatchNormalization(),
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

    # 5. Callbacks: Early Stopping (Slide 13) and Model Checkpoint
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True, verbose=1),
        ModelCheckpoint(
            filepath=os.path.join(utils.MODELS_DIR, "fnn_model.keras"),
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

    # 6. Train the model
    print("Training FNN model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=150,
        batch_size=32,
        callbacks=callbacks,
        class_weight=class_weight_dict
    )

    # 7. Evaluate the model
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nFinal Test Accuracy: {test_acc:.4f}")
    print(f"Final Test Loss: {test_loss:.4f}")
    print("FNN model training completed successfully and saved to models/fnn_model.keras")

if __name__ == "__main__":
    train_fnn()
