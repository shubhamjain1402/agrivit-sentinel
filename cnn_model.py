"""
Pest Detection CNN Model Architecture
Author: Shubham Jain
Description: Custom convolutional neural network for multi-class pest classification
Model Design: Progressive feature extraction with batch normalization
Input: 64x64 RGB images of pest specimens
Output: 10-class pest classification (aphids, armyworm, beetle, etc.)
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Conv2D, MaxPooling2D, GlobalAveragePooling2D,
                                     Flatten, Dense, Dropout, BatchNormalization)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os

# ==================== Model Architecture Definition ====================
def build_pest_classifier(input_height=64, input_width=64, num_classes=10):
    """
    Constructs a custom CNN for pest detection with optimized architecture
    
    Args:
        input_height: Input image height (default: 64)
        input_width: Input image width (default: 64)
        num_classes: Number of pest categories (default: 10)
    
    Returns:
        Compiled Keras Sequential model with batch normalization and dropout
    """
    
    model = Sequential()
    
    # ===== Stage 1: Initial Feature Extraction =====
    # Learns low-level features (edges, textures, basic patterns)
    model.add(Conv2D(
        filters=32,
        kernel_size=(3, 3),
        activation='relu',
        padding='same',
        input_shape=(input_height, input_width, 3),
        name='conv_extract_1'
    ))
    model.add(BatchNormalization())
    
    model.add(Conv2D(
        filters=32,
        kernel_size=(3, 3),
        activation='relu',
        padding='same',
        name='conv_extract_2'
    ))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # ===== Stage 2: Mid-Level Feature Extraction =====
    # Learns mid-level patterns (shapes, textures, combinations)
    model.add(Conv2D(
        filters=64,
        kernel_size=(3, 3),
        activation='relu',
        padding='same',
        name='conv_process_1'
    ))
    model.add(BatchNormalization())
    
    model.add(Conv2D(
        filters=64,
        kernel_size=(3, 3),
        activation='relu',
        padding='same',
        name='conv_process_2'
    ))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # ===== Stage 3: High-Level Feature Extraction =====
    # Learns complex features (object components, specific patterns)
    model.add(Conv2D(
        filters=128,
        kernel_size=(3, 3),
        activation='relu',
        padding='same',
        name='conv_abstract_1'
    ))
    model.add(BatchNormalization())
    
    model.add(Conv2D(
        filters=128,
        kernel_size=(3, 3),
        activation='relu',
        padding='same',
        name='conv_abstract_2'
    ))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    # ===== Feature Aggregation and Classification =====
    model.add(GlobalAveragePooling2D())
    
    # Dense classification layers with dropout regularization
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.4))
    
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.4))
    
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    
    # Output layer with softmax for multi-class distribution
    model.add(Dense(num_classes, activation='softmax'))
    
    # Compile with adaptive learning rate optimizer
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# ==================== Data Augmentation Pipeline ====================
def create_augmented_generators():
    """
    Creates data augmentation generators for training and validation
    Augmentation techniques prevent overfitting and improve generalization
    """
    
    # Training augmentation: aggressive transformations
    training_generator = ImageDataGenerator(
        rescale=1.0/255.0,              # Normalize to [0, 1]
        rotation_range=30,              # Random rotation ±30°
        width_shift_range=0.2,          # Horizontal shift 20%
        height_shift_range=0.2,         # Vertical shift 20%
        shear_range=0.15,               # Shear transformation
        zoom_range=0.2,                 # Random zoom 80-120%
        horizontal_flip=True,           # Enable horizontal flip
        fill_mode='nearest'
    )
    
    # Validation augmentation: normalization only
    validation_generator = ImageDataGenerator(rescale=1.0/255.0)
    
    return training_generator, validation_generator

# ==================== Model Training Function ====================
def train_pest_detection_model(
    data_dir='Data',
    save_path='pest_model_custom.keras',
    image_size=(64, 64),
    batch_size=32,
    epochs=50
):
    """
    Complete training pipeline for pest detection model
    
    Args:
        data_dir: Root data directory
        save_path: Output model path
        image_size: Input image dimensions
        batch_size: Training batch size
        epochs: Number of training epochs
    """
    
    train_path = os.path.join(data_dir, 'train')
    test_path = os.path.join(data_dir, 'test')
    
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training data not found at {train_path}")
    
    print("=" * 70)
    print("Pest Detection Model - Training Initialization")
    print("=" * 70)
    print(f"Input dimensions: {image_size[0]}x{image_size[1]}")
    print(f"Batch size: {batch_size}")
    print(f"Training epochs: {epochs}")
    print(f"Training dataset: {train_path}")
    print(f"Validation dataset: {test_path}")
    print("=" * 70)
    
    # Build model
    model = build_pest_classifier(
        input_height=image_size[0],
        input_width=image_size[1],
        num_classes=10
    )
    
    print("\nModel Architecture:")
    model.summary()
    
    # Create augmentation generators
    train_aug, val_aug = create_augmented_generators()
    
    # Load and preprocess training data
    train_loader = train_aug.flow_from_directory(
        train_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    # Load and preprocess validation data
    val_loader = val_aug.flow_from_directory(
        test_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    # Calculate steps
    num_train_samples = sum([len(os.listdir(os.path.join(train_path, d))) 
                             for d in os.listdir(train_path)])
    steps_per_epoch = max(1, num_train_samples // batch_size)
    
    # Train model
    print(f"\nStarting training: {epochs} epochs, {steps_per_epoch} steps/epoch...\n")
    training_results = model.fit(
        train_loader,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=val_loader,
        validation_steps=10
    )
    
    # Save model
    model.save(save_path)
    print(f"\nModel saved successfully: {save_path}")
    
    # Visualize results
    visualize_training_results(training_results)
    
    return model, training_results

# ==================== Results Visualization ====================
def visualize_training_results(history):
    """
    Creates plots of training and validation metrics
    """
    
    fig, subplots = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy visualization
    subplots[0].plot(history.history['accuracy'], 'b-', linewidth=2, label='Train Accuracy')
    subplots[0].plot(history.history['val_accuracy'], 'r-', linewidth=2, label='Validation Accuracy')
    subplots[0].set_title('Classification Accuracy', fontsize=14, fontweight='bold')
    subplots[0].set_xlabel('Epoch', fontsize=12)
    subplots[0].set_ylabel('Accuracy', fontsize=12)
    subplots[0].legend(fontsize=11)
    subplots[0].grid(True, alpha=0.3)
    
    # Loss visualization
    subplots[1].plot(history.history['loss'], 'b-', linewidth=2, label='Train Loss')
    subplots[1].plot(history.history['val_loss'], 'r-', linewidth=2, label='Validation Loss')
    subplots[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    subplots[1].set_xlabel('Epoch', fontsize=12)
    subplots[1].set_ylabel('Loss', fontsize=12)
    subplots[1].legend(fontsize=11)
    subplots[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pest_model_training_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("Training analysis plot saved as 'pest_model_training_analysis.png'")

# ==================== Main Execution ====================
if __name__ == '__main__':
    print("\n" + "="*70)
    print("PEST DETECTION CNN MODEL TRAINING SCRIPT")
    print("="*70 + "\n")
    
    # Execute training pipeline
    trained_model, history = train_pest_detection_model(
        data_dir='Data',
        save_path='pest_model_custom.keras',
        image_size=(64, 64),
        batch_size=32,
        epochs=50
    )
    
    print("\n" + "="*70)
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("="*70)









