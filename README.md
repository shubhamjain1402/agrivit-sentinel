# AgriVit Sentinel

AgriVit Sentinel is a Flask-based agricultural intelligence web app by **Shubham Jain**. It provides crop recommendation, fertilizer guidance, and pest image analysis workflows for farm decision support.

## Features

- Crop recommendation from soil and climate inputs.
- Fertilizer guidance from crop-specific NPK targets.
- Pest image upload and classification workflow.
- Responsive HTML templates for the main user flows.
- Production-ready Flask entry point for common hosting platforms.

## Project Links

- Author: [Shubham Jain](https://github.com/shubhamjain1402)
- Repository: `https://github.com/shubhamjain1402/agrivit-sentinel`

## Requirements

- Python 3.11 recommended
- pip
- A virtual environment

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open the app at:

```text
http://127.0.0.1:5000
```

## Deployment

This repo includes a `Procfile` for platforms that support Gunicorn:

```bash
web: gunicorn app:app
```

The app reads the `PORT` environment variable when deployed and falls back to port `5000` locally.

## Important Model Notes

- `Crop_Recommendation.pkl` is included and used for crop recommendations.
- Pest detection needs one of these model files in the project root:
  - `pest_model.keras`
  - `pest_model.h5`
  - `Trained_model_new.h5`
- Without a pest model file, the pest upload page will load, but image classification will return an unavailable-model error.

## Structure

```text
app.py                    Flask application
cnn_model.py              Pest model training/building utilities
crop_model.py             Crop model training utilities
Crop_Recommendation.pkl   Trained crop recommendation model
Data/Crop_NPK.csv         Crop nutrient targets for fertilizer guidance
static/                   CSS, images, uploads
templates/                Jinja templates
utils/fertilizer.py       Fertilizer recommendation text
```

## License

MIT License. Copyright (c) 2026 Shubham Jain.
