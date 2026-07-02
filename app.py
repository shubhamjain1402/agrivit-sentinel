"""
Agricultural Intelligence System - Flask Application
Author: Shubham Jain
Purpose: Integrated platform for crop, pest, and fertilizer management
Features: Deep learning-based pest detection, crop recommendation system, NPK analysis
"""

from flask import Flask, render_template, request, url_for
from markupsafe import Markup
from werkzeug.utils import secure_filename
import pandas as pd
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import pickle
from utils.fertilizer import get_nutrient_recommendations
import threading
import logging

# Configure logging for monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'user_uploaded')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# ==================== Model Loading Architecture ====================
class ModelManager:
    """Manages ML model lifecycle and thread-safe loading"""
    
    def __init__(self):
        self.pest_classifier = None
        self.crop_predictor = None
        self._model_lock = threading.Lock()
    
    def get_pest_model(self, preference_paths=None):
        """Load pest detection model with multiple fallback options"""
        if preference_paths is None:
            preference_paths = ['pest_model.keras', 'pest_model.h5', 'Trained_model_new.h5']

        if self.pest_classifier is not None:
            return self.pest_classifier
        
        with self._model_lock:
            if self.pest_classifier is not None:
                return self.pest_classifier
            
            for model_path in preference_paths:
                resolved_model_path = os.path.join(BASE_DIR, model_path)
                if not os.path.exists(resolved_model_path):
                    continue
                
                try:
                    self.pest_classifier = load_model(resolved_model_path)
                    logger.info(f"Pest model loaded: {model_path}")
                    return self.pest_classifier
                except Exception as e:
                    logger.warning(f"Model load failed ({model_path}): {str(e)}")
                    continue
            
            logger.error("No pest detection model available")
            return None
    
    def get_crop_model(self, model_path='Crop_Recommendation.pkl'):
        """Load crop recommendation ensemble model"""
        if self.crop_predictor is not None:
            return self.crop_predictor
        
        try:
            resolved_model_path = os.path.join(BASE_DIR, model_path)
            with open(resolved_model_path, 'rb') as f:
                self.crop_predictor = pickle.load(f)
                logger.info("Crop recommendation model loaded")
                return self.crop_predictor
        except Exception as e:
            logger.error(f"Crop model load failed: {str(e)}")
            return None

# Initialize model manager
model_mgr = ModelManager()

# ==================== Flask Application Setup ====================
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_image(filename):
    """Return True when an uploaded file has a supported image extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

# ==================== Nutrient Analysis Engine ====================
@app.route('/fertilizer-predict', methods=['POST'], endpoint='fertilizer_recommend')
def analyze_fertilizer_requirements():
    """
    Analyzes soil nutrient levels and provides personalized fertilizer recommendations
    """
    try:
        crop_name = str(request.form.get('cropname', '')).strip()
        nitrogen_current = int(request.form.get('nitrogen', 0))
        phosphorus_current = int(request.form.get('phosphorous', 0))
        potassium_current = int(request.form.get('potassium', 0))
        
        # Load crop NPK database
        npk_path = os.path.join(BASE_DIR, 'Data', 'Crop_NPK.csv')
        npk_data = pd.read_csv(npk_path)
        crop_row = npk_data[npk_data['Crop'] == crop_name]
        
        if crop_row.empty:
            return render_template('error_agrios.html', message='Crop not found in database')
        
        # Extract target nutrient values
        nitrogen_target = crop_row['N'].values[0]
        phosphorus_target = crop_row['P'].values[0]
        potassium_target = crop_row['K'].values[0]
        
        # Calculate deficiency levels
        nitrogen_gap = nitrogen_target - nitrogen_current
        phosphorus_gap = phosphorus_target - phosphorus_current
        potassium_gap = potassium_target - potassium_current
        
        # Determine fertilizer categories
        n_category = "excess_nitrogen" if nitrogen_gap < 0 else "nitrogen_deficient" if nitrogen_gap > 0 else "nitrogen_balanced"
        p_category = "excess_phosphorus" if phosphorus_gap < 0 else "phosphorus_deficient" if phosphorus_gap > 0 else "phosphorus_balanced"
        k_category = "excess_potassium" if potassium_gap < 0 else "potassium_deficient" if potassium_gap > 0 else "potassium_balanced"
        
        # Get recommendations
        n_recommendation = Markup(get_nutrient_recommendations(n_category))
        p_recommendation = Markup(get_nutrient_recommendations(p_category))
        k_recommendation = Markup(get_nutrient_recommendations(k_category))
        
        return render_template('Fertilizer-Result_agrios.html',
                               recommendation1=n_recommendation,
                               recommendation2=p_recommendation,
                               recommendation3=k_recommendation,
                               diff_n=abs(nitrogen_gap), 
                               diff_p=abs(phosphorus_gap), 
                               diff_k=abs(potassium_gap))
    except Exception as e:
        logger.error(f"Fertilizer analysis error: {str(e)}")
        return render_template('error_agrios.html', message='Error analyzing nutrient levels')

# ==================== Pest Detection Engine ====================
def predict_pest_species(image_path):
    """
    Advanced pest detection using deep learning
    Extracts model input dimensions dynamically for flexibility
    """
    try:
        model = model_mgr.get_pest_model()
        if model is None:
            logger.warning("Pest detection model unavailable")
            return 'unknown', None
        
        # Get model input specifications
        input_shape = model.input_shape  # (batch_size, height, width, channels)
        target_height = input_shape[1] if input_shape[1] else 128
        target_width = input_shape[2] if input_shape[2] else 128
        
        # Load and preprocess image
        loaded_image = image.load_img(image_path, target_size=(target_height, target_width))
        image_array = image.img_to_array(loaded_image)
        image_array = image_array / 255.0  # Normalize to [0, 1]
        image_array = np.expand_dims(image_array, axis=0)
        
        # Make prediction
        predictions = model.predict(image_array, verbose=0)
        predicted_class_idx = np.argmax(predictions, axis=1)[0]
        confidence_score = float(np.max(predictions))
        
        # Species mapping
        pest_species = ['aphids', 'armyworm', 'beetle', 'bollworm', 'earthworm',
                       'grasshopper', 'mites', 'mosquito', 'sawfly', 'stem_borer']
        predicted_species = pest_species[predicted_class_idx]
        
        logger.info(f"Detection: {predicted_species} (confidence: {confidence_score:.1%})")
        return predicted_class_idx, confidence_score
        
    except Exception as e:
        logger.error(f"Pest detection error: {str(e)}")
        return 'unknown', None

# ==================== Image Upload & Analysis Routes ====================
@app.route("/", endpoint='index')
@app.route("/index.html")
def home_page():
    """Landing page"""
    return render_template("index_agrios.html")

@app.route("/CropRecommendation.html")
def crop_recommendation_form():
    """Crop recommendation interface"""
    return render_template("CropRecommendation_agrios.html")

@app.route("/FertilizerRecommendation.html")
def fertilizer_form():
    """Fertilizer recommendation interface"""
    return render_template("FertilizerRecommendation_agrios.html")

@app.route("/PesticideRecommendation.html")
def pesticide_form():
    """Pest management interface"""
    return render_template("PesticideRecommendation_agrios.html")

@app.route("/predict", methods=['GET', 'POST'])
def upload_and_predict_pest():
    """
    Handles image upload and pest classification
    """
    if request.method == 'GET':
        return render_template("PesticideRecommendation_agrios.html")

    if request.method == 'POST':
        try:
            uploaded_file = request.files.get('image')
            if not uploaded_file or uploaded_file.filename == '':
                return render_template('error_agrios.html', message='No image file selected')

            if not allowed_image(uploaded_file.filename):
                return render_template('error_agrios.html', message='Please upload a PNG, JPG, JPEG, or WEBP image')
            
            # Save uploaded image
            file_name = secure_filename(uploaded_file.filename)
            save_directory = app.config['UPLOAD_FOLDER']
            os.makedirs(save_directory, exist_ok=True)
            save_path = os.path.join(save_directory, file_name)
            uploaded_file.save(save_path)
            
            # Get public URL
            image_url = url_for('static', filename=f"user_uploaded/{file_name}")
            
            logger.info(f"Processing uploaded image: {file_name}")
            
            # Perform pest detection
            pest_idx, confidence = predict_pest_species(save_path)
            
            if pest_idx == 'unknown':
                return render_template('error_agrios.html', 
                                      message='Unable to identify pest. Please try with a clearer image.')
            
            pest_species_list = ['aphids', 'armyworm', 'beetle', 'bollworm', 'earthworm',
                               'grasshopper', 'mites', 'mosquito', 'sawfly', 'stem_borer']
            detected_pest = pest_species_list[pest_idx]
            pest_display = detected_pest.replace('_', ' ')
            
            return render_template(
                f"{pest_display}_agrios.html",
                pred=pest_display,
                uploaded_image_url=image_url,
                confidence=f"{confidence:.1%}" if confidence else "N/A"
            )
        
        except Exception as e:
            logger.error(f"Pest prediction route error: {str(e)}")
            return render_template('error_agrios.html', message=f'Processing error: {str(e)}')

# ==================== Crop Prediction Engine ====================
@app.route('/crop_prediction', methods=['POST'])
def predict_suitable_crop():
    """
    Recommends optimal crop based on environmental and soil parameters
    Uses ensemble learning approach for robust predictions
    """
    try:
        crop_model = model_mgr.get_crop_model()
        if crop_model is None:
            return render_template('error_agrios.html', message="Crop prediction model unavailable")
        
        # Extract environmental parameters
        nitrogen = float(request.form.get('nitrogen', 0))
        phosphorus = float(request.form.get('phosphorous', 0))
        potassium = float(request.form.get('potassium', 0))
        soil_ph = float(request.form.get('ph', 0))
        rainfall_mm = float(request.form.get('rainfall', 0))
        avg_temperature = float(request.form.get('temperature', 0))
        relative_humidity = float(request.form.get('humidity', 0))
        
        # Prepare feature vector
        feature_vector = [nitrogen, phosphorus, potassium, avg_temperature, 
                         relative_humidity, soil_ph, rainfall_mm]
        default_feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        
        # Create dataframe and reorder if needed
        input_df = pd.DataFrame([feature_vector], columns=default_feature_names)
        
        if hasattr(crop_model, 'feature_names_in_'):
            feature_order = list(crop_model.feature_names_in_)
            input_df = input_df[feature_order]
        
        # Generate prediction
        crop_prediction = crop_model.predict(input_df)
        recommended_crop = crop_prediction[0]
        
        logger.info(f"Crop recommendation: {recommended_crop}")
        
        return render_template('crop-result_agrios.html',
                               prediction=recommended_crop,
                               pred=f'img/crop/{recommended_crop}.jpg')
    
    except Exception as e:
        logger.error(f"Crop prediction error: {str(e)}")
        return render_template('error_agrios.html', message="Prediction failed")

# ==================== Server Initialization ====================
if __name__ == '__main__':
    # Preload models in background thread
    threading.Thread(target=model_mgr.get_pest_model, daemon=True).start()
    threading.Thread(target=model_mgr.get_crop_model, daemon=True).start()
    
    logger.info("Starting Agricultural Intelligence System")
    debug_mode = os.environ.get('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode, use_reloader=False)
    
