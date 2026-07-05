# Sample Project Documentation (Technical Manual)

This document provides a technical manual and installation guide for the Human Development Index (HDI) Predictor.

---

## 🛠 Local Setup Instructions

### 1. Initialize Folder Structure & Setup Virtual Environment
Run the following commands inside PowerShell or Command Prompt:
```powershell
# Navigate to project workspace
cd C:\Users\User\.gemini\antigravity\scratch\hdi_predictor

# Initialize python virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### 2. Install Packages
Install dependencies from [`requirements.txt`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/requirements.txt):
```bash
python -m pip install -r requirements.txt
```

### 3. Run the Machine Learning Pipeline
Compile the dataset, generate visualizations, and fit the regression weights:
```bash
python train_model.py
```

### 4. Run the Web Application
Launch the Flask development server:
```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Testing the Solution

To run the automated tests verifying backend routing and model metrics:
```bash
python -m unittest discover -s tests
```

---

## 🚪 Authentication Details

The system is protected by a session cookie gate.
* **Username:** `admin` (pre-filled on screen)
* **Password:** `admin123` (pre-filled on screen)
* **Logout:** Click "Sign Out" in the sidebar or navbar to clear the session.
