"""
Crop Recommendation System - Ensemble Machine Learning Model
Author: Shubham Jain
Purpose: Predict optimal crop based on environmental and soil parameters
Approach: Voting ensemble combining SVM, Random Forest, and KNN classifiers
Features: N, P, K (nutrients), Temperature, Humidity, pH, Rainfall
Output: Recommended crop type
"""

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import pickle
import numpy as np

# ==================== Data Loading and Preparation ====================
def load_and_prepare_data(csv_path='Data/crop_recommendation.csv', test_size=0.15):
    """
    Loads crop recommendation dataset and prepares train-test split
    
    Args:
        csv_path: Path to crop recommendation CSV
        test_size: Test set proportion (default: 15%)
    
    Returns:
        X_train, X_test, y_train, y_test: Split datasets
    """
    
    print("Loading crop recommendation dataset...")
    dataset = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {dataset.shape}")
    print(f"Features: {list(dataset.columns[:-1])}")
    print(f"Target classes: {dataset.iloc[:, -1].unique()}")
    
    # Separate features and target
    features = dataset.iloc[:, :-1].values
    target = dataset.iloc[:, -1].values
    
    # Split data: 85% training, 15% testing
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, 
        test_size=test_size, 
        random_state=42,
        stratify=target  # Maintain class distribution
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test

# ==================== Ensemble Classifier Construction ====================
def build_voting_ensemble():
    """
    Creates a weighted voting ensemble of diverse classifiers
    Each classifier brings different learning perspectives
    
    Classifiers:
    - SVM: Multiple kernel variants for non-linear decision boundaries
    - Random Forest: Ensemble of decision trees
    - KNN: Instance-based learning with varying k values
    - Naive Bayes: Probabilistic classifier
    """
    
    classifiers = []
    
    # ===== Support Vector Machines =====
    # Linear SVM with automatic gamma
    classifiers.append(('svm_rbf', SVC(
        kernel='rbf',
        gamma='auto',
        probability=True,
        C=1.0
    )))
    
    # SVM with polynomial kernels (degrees 2-4)
    classifiers.append(('svm_poly2', SVC(
        kernel='poly',
        degree=2,
        probability=True,
        C=1.0
    )))
    
    classifiers.append(('svm_poly3', SVC(
        kernel='poly',
        degree=3,
        probability=True,
        C=1.0
    )))
    
    classifiers.append(('svm_poly4', SVC(
        kernel='poly',
        degree=4,
        probability=True,
        C=0.8  # Reduced C to prevent overfitting
    )))
    
    # ===== Random Forest =====
    classifiers.append(('random_forest', RandomForestClassifier(
        n_estimators=150,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )))
    
    # ===== K-Nearest Neighbors =====
    # Different k values for diversity
    classifiers.append(('knn_k3', KNeighborsClassifier(
        n_neighbors=3,
        weights='uniform',
        metric='euclidean'
    )))
    
    classifiers.append(('knn_k5', KNeighborsClassifier(
        n_neighbors=5,
        weights='distance',
        metric='euclidean'
    )))
    
    classifiers.append(('knn_k7', KNeighborsClassifier(
        n_neighbors=7,
        weights='distance',
        metric='euclidean'
    )))
    
    classifiers.append(('knn_k9', KNeighborsClassifier(
        n_neighbors=9,
        weights='distance',
        metric='euclidean'
    )))
    
    # ===== Naive Bayes =====
    classifiers.append(('naive_bayes', GaussianNB()))
    
    # Create voting ensemble with soft voting (probability averaging)
    ensemble = VotingClassifier(
        estimators=classifiers,
        voting='soft'  # Use probability predictions for voting
    )
    
    return ensemble

# ==================== Model Training Pipeline ====================
def train_crop_recommendation_model(
    csv_path='Data/crop_recommendation.csv',
    output_model='Crop_Recommendation_Custom.pkl',
    test_size=0.15
):
    """
    Complete training pipeline for crop recommendation ensemble
    
    Args:
        csv_path: Input dataset path
        output_model: Output model file path
        test_size: Test set proportion
    """
    
    print("\n" + "="*70)
    print("CROP RECOMMENDATION ENSEMBLE MODEL TRAINING")
    print("="*70 + "\n")
    
    # Load and prepare data
    X_train, X_test, y_train, y_test = load_and_prepare_data(csv_path, test_size)
    
    # Feature scaling (important for SVM and KNN)
    print("\nScaling features to normalize value ranges...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build ensemble
    print("\nBuilding voting ensemble with 9 diverse classifiers...")
    ensemble_model = build_voting_ensemble()
    
    # Train ensemble
    print("\nTraining ensemble on scaled features...")
    ensemble_model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = ensemble_model.predict(X_test_scaled)
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest Set Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Cross-validation
    print("\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(ensemble_model, X_train_scaled, y_train, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Classification report
    print("\n" + "-"*70)
    print("CLASSIFICATION REPORT")
    print("-"*70)
    print(classification_report(y_test, y_pred))
    
    # Save model and scaler
    model_package = {
        'ensemble': ensemble_model,
        'scaler': scaler
    }
    
    with open(output_model, 'wb') as f:
        pickle.dump(model_package, f)
    
    print(f"Model saved: {output_model}")
    
    # Store feature names for inference
    feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    ensemble_model.feature_names_in_ = np.array(feature_names)
    
    print("\n" + "="*70)
    print("TRAINING COMPLETED")
    print("="*70 + "\n")
    
    return ensemble_model, scaler

# ==================== Individual Classifier Performance Comparison ====================
def evaluate_individual_classifiers(X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled):
    """
    Evaluates individual classifier performance for comparison
    """
    
    print("\n" + "="*70)
    print("INDIVIDUAL CLASSIFIER PERFORMANCE COMPARISON")
    print("="*70 + "\n")
    
    classifiers_to_test = [
        ('SVM (RBF)', SVC(kernel='rbf', gamma='auto', probability=True)),
        ('SVM (Poly-3)', SVC(kernel='poly', degree=3, probability=True)),
        ('Random Forest', RandomForestClassifier(n_estimators=150, random_state=42)),
        ('KNN (k=5)', KNeighborsClassifier(n_neighbors=5)),
        ('KNN (k=7)', KNeighborsClassifier(n_neighbors=7)),
        ('Naive Bayes', GaussianNB()),
    ]
    
    for name, clf in classifiers_to_test:
        if name == 'Naive Bayes':
            clf.fit(X_train, y_train)
            accuracy = clf.score(X_test, y_test)
        else:
            clf.fit(X_train_scaled, y_train)
            accuracy = clf.score(X_test_scaled, y_test)
        
        print(f"{name:20} - Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

# ==================== Main Execution ====================
if __name__ == '__main__':
    # Train the ensemble model
    trained_ensemble, fitted_scaler = train_crop_recommendation_model(
        csv_path='Data/crop_recommendation.csv',
        output_model='Crop_Recommendation_Custom.pkl',
        test_size=0.15
    )
    
    print("\nCrop recommendation model ready for deployment!")
