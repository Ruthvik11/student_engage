from pymongo import MongoClient
import pandas as pd
import random
mongo_uri = "mongodb+srv://ruthvik:Ruthvik6660@cluster0.vay81.mongodb.net/"
client = MongoClient(mongo_uri)
db = client["student_engagement"]

raw_data_collection = db["raw_data"]
processed_data_collection = db["processed_data"]

if raw_data_collection.count_documents({}) == 0:
    stud_data = pd.read_csv("raw/online_course_engagement_data.csv")
    stud_data_dict = stud_data.to_dict(orient='records')
    raw_data_collection.insert_many(stud_data_dict)
    print(" Raw dataset successfully stored in MongoDB!")
else:
    print(" Raw data already exists, skipping insertion.")

def insert_raw_data(input_data):
    existing_ids = {user["UserId"] for user in get_raw_data() if "UserId" in user}

    for doc in input_data:
        doc.pop('_id', None)  # Remove `_id` if present (prevents duplicate key errors)

        # ✅ Ensure `UserId` is assigned if missing
        if "UserId" not in doc or pd.isna(doc["UserId"]):
            while True:
                new_id = random.randint(1000, 9999)  # Generate unique 4-digit UserId
                if new_id not in existing_ids:
                    doc["UserId"] = new_id
                    existing_ids.add(new_id)  # Update existing IDs set
                    break  

    raw_data_collection.insert_many(input_data)

def get_raw_data():
    return list(raw_data_collection.find({}, {"_id": 0}))

def insert_processed_data(processed_data):
    processed_data_collection.delete_many({})  # Clear existing data
    for doc in processed_data:
        doc.pop('_id', None)  # Remove _id if present
    processed_data_collection.insert_many(processed_data)


def get_processed_data():
    return list(processed_data_collection.find({}, {"_id": 0}))