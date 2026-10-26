from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE = Path(__file__).parent
DATA = BASE / "data" / "travel_time_dataset.csv"
app = Flask(__name__, static_folder="frontend", static_url_path="")

df = pd.read_csv(DATA)
df["time_hour"] = df["time_of_day"].str.split(":").str[0].astype(float)

features = ["distance_km","traffic_level","time_hour","road_type","weather","avg_speed_kmph"]
target = "travel_time_min"

X, y = df[features], df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

cat = ["traffic_level","road_type","weather"]
num = ["distance_km","time_hour","avg_speed_kmph"]
prep = ColumnTransformer([
    ("num", StandardScaler(), num),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat)
])

ridge_model = Pipeline([("prep", prep),("model", Ridge(alpha=1.0))])
lasso_model = Pipeline([("prep", prep),("model", Lasso(alpha=.05,max_iter=10000))])
ridge_model.fit(X_train,y_train)
lasso_model.fit(X_train,y_train)

def metrics(model):
    p=model.predict(X_test)
    return {"mae":mean_absolute_error(y_test,p),
            "mse":mean_squared_error(y_test,p),
            "rmse":np.sqrt(mean_squared_error(y_test,p)),
            "r2":r2_score(y_test,p)}

@app.get("/api/metrics")
def get_metrics():
    return jsonify({"ridge":metrics(ridge_model),"lasso":metrics(lasso_model),"rows":len(df)})

@app.post("/api/predict")
def predict():
    d=request.get_json()
    hour=int(str(d["time"]).split(":")[0])
    row=pd.DataFrame([{
      "distance_km":float(d["distance"]),
      "traffic_level":d["traffic"],
      "time_hour":hour,
      "road_type":d["road"],
      "weather":d["weather"],
      "avg_speed_kmph":float(d.get("speed",32))
    }])
    r=float(ridge_model.predict(row)[0]); l=float(lasso_model.predict(row)[0])
    return jsonify({"ridge":round(r,2),"lasso":round(l,2),"average":round((r+l)/2,2)})

@app.get("/")
def index(): return send_from_directory(app.static_folder,"index.html")

if __name__=="__main__":
    app.run(debug=True)
