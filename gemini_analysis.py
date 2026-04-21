import os
import time
import firebase_admin
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from firebase_admin import credentials, firestore

# --- 1. CONFIGURATION ---
# Load environment variables from the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_KEY_PATH")

# Safety Check: Ensure keys are loaded
if not GEMINI_API_KEY or not SERVICE_ACCOUNT_PATH:
    print("❌ Error: GEMINI_API_KEY or FIREBASE_KEY_PATH not found in .env file.")
    exit()

# --- 2. INITIALIZATION ---
client = genai.Client(api_key=GEMINI_API_KEY)

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"❌ Firebase Auth Error: {e}")
        exit()
        
db = firestore.client()

# --- 3. FETCH & CLEAN DATA ---
print("📡 Fetching subgrid data from Firestore...")
try:
    # Limit to 20 to stay within Free Tier token limits
    docs = db.collection('subgrids_data').limit(20).stream()

    data_list = []
    for doc in docs:
        d = doc.to_dict()
        # Cleaning data: Keep only the metrics for optimization
        essential_data = {
            "id": doc.id,
            "v": d.get("voltage"),
            "i": d.get("current"),
            "load": d.get("load"),
            "ts": str(d.get("timestamp")) 
        }
        data_list.append(essential_data)
except Exception as e:
    print(f"❌ Firestore Data Error: {e}")
    exit()

if not data_list:
    print("⚠️ No data found in Firestore collection 'subgrids_data'.")
    exit()

# --- 4. CREATE PROMPT ---
prompt = f"""
You are an energy optimization AI specialized in Microgrids.

Analyze the following subgrid data and provide a concise report:
1. System Stability Assessment
2. List of specific anomalies (if any)
3. Actionable optimization suggestions to reduce waste

Data:
{data_list}
"""

# --- 5. EXECUTE WITH RETRY LOGIC ---
print(f"🤖 Sending {len(data_list)} records to Gemini-2.5-Flash-Lite...")

def get_analysis():
    for attempt in range(3):
        try:
            # Using the 'lite' model for better daily quota limits
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=prompt
            )
            return response.text
        except errors.ClientError as e:
            if e.status_code == 429:
                wait_time = 30 * (attempt + 1)
                print(f"⏳ Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                return f"❌ API Error: {e.message}"
        except Exception as e:
            return f"❌ Unexpected Error: {e}"
    return "❌ Failed after multiple attempts due to quota limits."

# --- 6. OUTPUT ---
analysis_result = get_analysis()
print("\n" + "="*40)
print("🔍 ECOFLOW ENERGY ANALYSIS REPORT")
print("="*40 + "\n")
print(analysis_result)