# API Notes

AgriVit Sentinel is primarily a Flask web application that returns HTML pages.

## Base URL

```text
http://localhost:5000
```

## Routes

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | GET | Home page |
| `/CropRecommendation.html` | GET | Crop recommendation form |
| `/crop_prediction` | POST | Submit crop inputs |
| `/FertilizerRecommendation.html` | GET | Fertilizer form |
| `/fertilizer-predict` | POST | Submit fertilizer inputs |
| `/PesticideRecommendation.html` | GET | Pest upload form |
| `/predict` | GET/POST | Pest upload and prediction |

## Owner

- GitHub: [shubhamjain1402](https://github.com/shubhamjain1402)
- Repository: `https://github.com/shubhamjain1402/agrivit-sentinel`
