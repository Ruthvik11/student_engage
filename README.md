# 🎓 Student Engagement Prediction API

A FastAPI-based machine learning project to **analyze and predict student engagement levels** in online education platforms using behavioral and performance data.

## 🚀 Features

- Upload raw student data via API
- Perform ETL (Extract, Transform, Load) operations
- Feature engineering (Engagement Score, Engagement Level)
- Label and one-hot encoding
- Store raw and processed data in MongoDB
- Train ML models dynamically using processed data
- Predict engagement levels: **Low**, **Medium**, **High**
- Automatically store prediction inputs for future training

## 🧠 Engagement Classification

Based on student activity, the project classifies engagement into:

- 📉 Low
- 📊 Medium
- 📈 High

## 🗂️ Tech Stack

- **Backend:** FastAPI
- **Database:** MongoDB
- **ML Model:** RandomForestClassifier (GridSearchCV tuned)
- **Others:** Pandas, Scikit-learn, Pydantic, Uvicorn

## 📦 API Endpoints

| Method | Endpoint           | Description                              |
|--------|--------------------|------------------------------------------|
| POST   | `/upload-data`     | Upload raw student engagement data       |
| POST   | `/run-etl`         | Run the ETL pipeline                     |
| POST   | `/train-model`     | Train ML model on processed data         |
| POST   | `/predict`         | Predict engagement level for new input   |

## ⚙️ ETL Workflow

1. **Extract:** Get raw data from MongoDB
2. **Transform:** 
   - Handle missing values
   - Create `Engagement Score`
   - Derive `Engagement Level` (Low, Medium, High)
   - Encode categorical features
3. **Load:** Store processed data back to MongoDB

## 🏋️‍♂️ Model Training

- Fetches processed data from MongoDB
- Trains a RandomForestClassifier
- Saves model for future predictions

## 🔮 Prediction Example

```json
POST /predict
{
  "Feature1": value,
  "Feature2": value,
  ...
}
