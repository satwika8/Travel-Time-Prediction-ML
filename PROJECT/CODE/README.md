# TravelPredict Pro

A complete academic demonstration website for:
Travel Time Prediction Using Ridge and Lasso Regression.

The supplied project documents specify the project concept, Ridge/Lasso algorithms,
travel-related features and MAE/MSE/RMSE/R² evaluation. They do not specify an
original dataset. This package therefore contains a clearly labelled synthetic
1,000-row dataset created for academic demonstration.

## Files
- frontend/index.html — professional website
- frontend/style.css — UI
- frontend/script.js — browser interaction
- data/travel_time_dataset.csv — synthetic dataset (1,000 trips)
- app.py — real Scikit-learn Ridge/Lasso backend
- requirements.txt — Python dependencies

## Run the real ML website
1. Install Python 3.x.
2. Open terminal in this folder.
3. Run: pip install -r requirements.txt
4. Run: python app.py
5. Open http://127.0.0.1:5000

The backend trains both Ridge and Lasso from the included CSV and exposes:
GET /api/metrics
POST /api/predict

## Academic note
Do not describe this synthetic dataset as collected real-world traffic data.
In the report/presentation say that a synthetic dataset was used because the
provided project documents did not specify an original dataset source.
