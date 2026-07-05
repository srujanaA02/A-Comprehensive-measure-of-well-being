# Coding & Solution Overview

This document presents a code inventory and summarizes the core implementation behind the Human Development Index (HDI) Predictor system.

---

## 🛠 Project Code Inventory

The solution is split into modular scripts:

1. **[`config.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/config.py):** Encapsulates environment configurations, directories setup, and paths to raw and processed datasets.
2. **[`train_model.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/train_model.py):**
   * Downloads raw UNDP datasets.
   * Runs preprocessing to melt indicator matrices into a long tidy table structure.
   * Generates Seaborn/Matplotlib visualization plots.
   * Standardizes features and trains a multi-variate Linear Regression model.
   * Serializes model and standard scaler.
3. **[`app.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/app.py):**
   * Configures Flask server routes, error overrides, and auth cookies.
   * Intercepts unauthenticated dashboard requests, redirecting them to `/login`.
   * Serves static metrics and handles predictions form POST.
   * Runs StandardScaler standardization and predicts index values.
   * Determines HDI categories and recommends policy actions.
4. **[`script.js`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/static/js/script.js):**
   * Syncs sliders with input forms.
   * Manages light/dark mode storage preferences.
   * Drives country select prefills.
   * Persists client histories and processes CSV exports.
5. **[`style.css`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/static/css/style.css):**
   * Contains HSL-based colors mapping Light and Dark themes.
   * Applies glassmorphism design tokens (`backdrop-filter`).
   * Configures printer layouts to hide sidebars when printing report cards.

---

## 💻 Source Code Accessibility

All active code files are located within the root project workspace at `C:\Users\User\.gemini\antigravity\scratch\hdi_predictor`. You can browse and edit them directly.
The automated unit tests in [`tests/`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/tests) verify model training outputs and Flask routes.
