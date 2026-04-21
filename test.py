import firebase_admin
from firebase_admin import credentials, firestore
import random
import time

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Add multiple documents
for i in range(5):
    doc_ref = db.collection("sensor_data").document()
    doc_ref.set({
        "temperature": random.randint(20, 40),
        "humidity": random.randint(30, 80),
        "timestamp": time.time()
    })
    print(f"Data {i+1} added")

print("✅ Multiple data sent!")



# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Firebase
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# # Connect to Firestore
# db = firestore.client()

# # Test: Add data
# doc_ref = db.collection("test_collection").document("test_doc")
# doc_ref.set({
#     "message": "Hello Firebase!",
#     "status": "connected"
# })

# print("✅ Data sent to Firestore successfully!")


# from google import genai

# # Initialize the client
# client = genai.Client(api_key='AIzaSyBc8YmNdtFqp8cvDroaySnTA-Uq67sdqCo')

# print("Fetching available models...")
# print("-" * 30)

# try:
#     # Iterate through the models
#     for model in client.models.list():
#         print(f"Model ID: {model.name}")
#         # Note: 'supported_methods' is the correct attribute in the new SDK
#         print(f"Capabilities: {model.supported_methods}")
#         print("-" * 30)
# except Exception as e:
#     print(f"An error occurred: {e}")