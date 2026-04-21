import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import time
import random

# --- 1. INITIALIZE FIREBASE ---
load_dotenv()  # Load variables from .env

# Get path from environment variable
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_KEY_PATH")

if not SERVICE_ACCOUNT_PATH:
    print("❌ Error: FIREBASE_KEY_PATH not found in .env file.")
    exit()

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


 # --- 1. INITIALIZE FIREBASE ---
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# --- 2. DEFINE FIELD CATEGORIES ---
SHARED_FIELDS = [
    'timestamp', 'temperature', 'humidity', 'cloud_cover', 
    'solar_irradiance', 'wind_speed', 'electricity_price', 
    'grid_frequency', 'voltage_level'
]

SPLIT_FIELDS = [
    'load_demand', 'solar_power_output', 'wind_power_output', 
    'total_power_generation', 'grid_import_power', 'grid_export_power', 
    'battery_soc'
]

def run_simulation():
    # --- 3. LOAD DATA ---
    df = pd.read_csv('demo_data.csv')

    # --- 4. CONVERT TIMESTAMP ---
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- 5. FILTER FIRST 2 DAYS ---
    df = df.sort_values('timestamp')

    start_date = df['timestamp'].min()
    end_date = start_date + pd.Timedelta(days=2)

    df_filtered = df[
        (df['timestamp'] >= start_date) &
        (df['timestamp'] < end_date)
    ]

    print(f"🚀 Simulation Started for 2 days ({len(df_filtered)} rows)...")

    # --- 6. LOOP THROUGH DATA ---
    for index, row in df_filtered.iterrows():

        # Generate weights (sum = 1)
        raw_weights = [random.uniform(0.1, 1.0) for _ in range(5)]
        total = sum(raw_weights)
        weights = [w / total for w in raw_weights]

        # --- 7. PROCESS EACH SUBGRID ---
        for i in range(5):
            subgrid_id = f"subgrid_{i+1}"
            subgrid_data = {}

            # Shared fields
            for field in SHARED_FIELDS:
                subgrid_data[field] = row[field]

            # Split fields
            for field in SPLIT_FIELDS:
                subgrid_data[field] = round(row[field] * weights[i], 2)

            # --- IMPORTANT FOR FLAT STRUCTURE ---
            subgrid_data['subgrid_id'] = subgrid_id
            subgrid_data['row_index'] = index
            subgrid_data['last_updated'] = firestore.SERVER_TIMESTAMP

            # --- UNIQUE DOCUMENT ID ---
            doc_id = f"{subgrid_id}_{index}"

            # --- PUSH TO FIREBASE (FLAT COLLECTION) ---
            db.collection('subgrids_data').document(doc_id).set(subgrid_data)

        print(f"✅ Row {index} pushed")

        # Fast simulation
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user.")
        