import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# --- FIREBASE SETUP ---
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# --- FETCH DATA ---
docs = db.collection('subgrids_data').stream()

data = []
for doc in docs:
    data.append(doc.to_dict())

# --- CONVERT TO DATAFRAME ---
df = pd.DataFrame(data)

# --- SAVE TO CSV ---
df.to_csv("energy_data.csv", index=False)

print("CSV file created: energy_data.csv")