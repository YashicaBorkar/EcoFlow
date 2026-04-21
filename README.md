# EcoFlow

Setup Instructions
1. Clone the repository
git clone https://github.com/YashicaBorkar/EcoFlow.git
cd EcoFlow
2. Install dependencies
pip install -r requirements.txt

If requirements.txt is not available:

pip install firebase-admin pandas python-dotenv google-genai
3. Create environment file

Create a file named .env in the root directory:

GEMINI_API_KEY=your_api_key_here
FIREBASE_KEY_PATH=serviceAccountKey.json
Gemini API Setup
Go to: https://aistudio.google.com/
Click on "Get API Key"
Create a new API key
Copy and paste it into the .env file
Firebase Setup
Go to: https://console.firebase.google.com/
Create a new project
Open Project Settings
Go to the "Service Accounts" tab
Click "Generate new private key"
Download the JSON file

Place the file in your project directory and ensure the name matches the path in .env.

Running the Project
Step 1: Push data to Firebase
python main.py

This will:

Process the dataset
Simulate energy distribution across subgrids
Store data in Firestore
Step 2: Run AI analysis
python gemini_analysis.py

This will:

Fetch recent data from Firebase
Send it to Gemini
Print analysis including stability, anomalies, and optimization suggestions
Data Design

The project uses a flat Firestore structure:

subgrids_data
   ├── document_1
   ├── document_2
   ├── document_3

Each document contains:

subgrid_id
timestamp
energy parameters (solar, wind, load, etc.)

This design ensures efficient querying and compatibility with AI processing.
