import pandas as pd
import random
from sklearn.preprocessing import LabelEncoder
from .database import get_processed_data, get_raw_data, insert_raw_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def train_model():
    global feature_names
    processed_data = get_processed_data()

    processed_data = pd.DataFrame(processed_data)

    print(processed_data.head(5))
    labeled_data = processed_data.dropna(subset=["CourseCompletion","UserID"])  # Remove NaNs
    unlabeled_data = processed_data[processed_data["CourseCompletion"].isna()]

    # Drop UserID before training - it shouldn't be a feature
    x = labeled_data.drop(columns=["CourseCompletion", "UserID"])
    y = labeled_data["CourseCompletion"].astype(int) 

    global feature_names
    feature_names = x.columns.tolist()  # Now feature_names won't include UserID
    print(feature_names)
    print(y)
    global rc_model
    rc_model = RandomForestClassifier(n_estimators=100, random_state=42)

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2, random_state=42,stratify=y)

    print(x_train.shape)
    print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    rc_model.fit(x_train,y_train)

    print("model trained successfully")


def predict_coursecompletion(input_data):
    global rc_model  

    
    
     
    input_dataframe = pd.DataFrame([input_data])
    
    print(input_dataframe)
    
    w_time =  0.18  
    w_videos = 0.23  
    w_quizzes = 0.28  
    w_quiz_scores = 0.30
  

    input_dataframe["EngagementScore"] = (
        (w_time * input_dataframe["TimeSpentOnCourse"]) +
        (w_videos * input_dataframe["NumberOfVideosWatched"]) +
        (w_quizzes * input_dataframe["NumberOfQuizzesTaken"]) +
        (w_quiz_scores * input_dataframe["QuizScores"]) 
    )

    processed_data = get_processed_data()
    processed_dataframe = pd.DataFrame(processed_data)
    Q1 = processed_dataframe["EngagementScore"].quantile(0.25)
    Q3 = processed_dataframe["EngagementScore"].quantile(0.75)

    def label(score):
        if score < Q1:
            return "Low"
        elif Q1 <= score <= Q3:
            return "Medium"
        else:
            return "High"
    engagement_level_text = label(input_dataframe["EngagementScore"].iloc[0])
    input_dataframe["EngagementLevel"] = input_dataframe["EngagementScore"].apply(label)
    
    le = LabelEncoder()
    input_dataframe["EngagementLevel"] = le.fit_transform(input_dataframe["EngagementLevel"]) 

    input_dataframe = pd.get_dummies(input_dataframe, columns=["CourseCategory"], drop_first=False)

    
    for col in input_dataframe.columns:
        if input_dataframe[col].dtype == 'bool':
            input_dataframe[col] = input_dataframe[col].astype(int)
            
    
    if "UserID" in input_dataframe.columns:
        input_dataframe = input_dataframe.drop(columns=["UserID"])
    
    global feature_names
    for col in feature_names:
        if col not in input_dataframe.columns:
            input_dataframe[col] = 0  

    
    missing_cols = set(feature_names) - set(input_dataframe.columns)
    for col in missing_cols:
        input_dataframe[col] = 0  
        
    
    extra_cols = set(input_dataframe.columns) - set(feature_names)
    if extra_cols:
        input_dataframe = input_dataframe.drop(columns=list(extra_cols))
        
    
    input_dataframe = input_dataframe[feature_names]
    
    
    if "rc_model" not in globals():
        return {"error": " Model is not trained. Please train it first."}

    
    try:
        prediction = rc_model.predict(input_dataframe)

        
        input_data["CourseCompletion"] = int(prediction[0])
        
        

        return {
            "PredictedCourseCompletion": int(prediction[0]),
            "EngagementScore": float(input_dataframe["EngagementScore"].iloc[0]),
            "EngagementLevel": engagement_level_text
        }

    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}








