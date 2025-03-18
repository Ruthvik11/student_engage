import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from database import get_raw_data, insert_processed_data

# 1. Calculate Engagement Score
def calculate_engagement_score(raw_dataframe):
    w_time = 0.3  
    w_videos = 0.2  
    w_quizzes = 0.2  
    w_quiz_scores = 0.2  

    raw_dataframe["EngagementScore"] = (
        (w_time * raw_dataframe["TimeSpentOnCourse"]) +
        (w_videos * raw_dataframe["NumberOfVideosWatched"]) +
        (w_quizzes * raw_dataframe["NumberOfQuizzesTaken"]) +
        (w_quiz_scores * raw_dataframe["QuizScores"]) 
    )
    return raw_dataframe

# 2. Classify Engagement Levels
def classify_engagement(raw_dataframe):
    Q1 = raw_dataframe["EngagementScore"].quantile(0.25)
    Q3 = raw_dataframe["EngagementScore"].quantile(0.75)

    def label(score):
        if score < Q1:
            return "Low"
        elif Q1 <= score <= Q3:
            return "Medium"
        else:
            return "High"

    raw_dataframe["EngagementLevel"] = raw_dataframe["EngagementScore"].apply(label)
    return raw_dataframe

# 3. Encode Engagement Level
def encode_engagement_level(raw_dataframe):
    le = LabelEncoder()
    raw_dataframe["EngagementLevel"] = le.fit_transform(raw_dataframe["EngagementLevel"])  
    return raw_dataframe

# 4. One-Hot Encode Course Category
def one_hot_encode_course(raw_dataframe):
    raw_dataframe = pd.get_dummies(raw_dataframe, columns=["CourseCategory"], drop_first=False)

    # Convert boolean columns (True/False) to integers (0/1)
    for col in raw_dataframe.columns:
        if raw_dataframe[col].dtype == 'bool':
            raw_dataframe[col] = raw_dataframe[col].astype(int)
    return raw_dataframe

# 5. ETL Pipeline
def run_etl():
    raw_data = get_raw_data()
    raw_dataframe = pd.DataFrame(raw_data)

    print("Raw DataFrame Columns Before Processing:", raw_dataframe.columns)  # Debugging step

    raw_dataframe = calculate_engagement_score(raw_dataframe)
    raw_dataframe = classify_engagement(raw_dataframe)
    raw_dataframe = encode_engagement_level(raw_dataframe)
    raw_dataframe = one_hot_encode_course(raw_dataframe)

    print(raw_dataframe.head(5))  
    print(raw_dataframe.info())  

    processed_data = raw_dataframe.to_dict(orient="records")
    insert_processed_data(processed_data)

    print("Processed Data Inserted Successfully!")
