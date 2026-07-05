# Project Executable Files

This document lists all the executable scripts, source codes, templates, and binary assets that form our complete project solution.

---

## 📂 Codebase Inventory & Paths

All files are stored in the active project workspace directory: `C:\Users\User\.gemini\antigravity\scratch\hdi_predictor`.

### 1. Executable Python Scripts
* **[`app.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/app.py):** The web application server entry point. Configures routing logic, validations, and logs.
* **[`train_model.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/train_model.py):** The ML pipeline. Runs raw ingestion, pre-processing, plotting, and linear fitting.

### 2. Configurations & Packages
* **[`config.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/config.py):** Central configuration parameters class.
* **[`requirements.txt`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/requirements.txt):** List of Python libraries required for runtime operations.
* **[`.gitignore`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/.gitignore):** Standard Git ignore configuration.

### 3. Visualizations & Binary Assets
* **Model Binaries (`models/`):**
  * `hdi_model.pkl`: Serialized Linear Regression model parameters.
  * `scaler.pkl`: Serialized StandardScaler binary.
* **Data Sheets (`dataset/`):**
  * `hdi_raw.csv`: Raw downloaded UN statistical metrics.
  * `hdi_processed.csv`: Cleaned panel format dataset.
* **Plots (`static/plots/`):**
  * `correlation_matrix.png`, `hdi_distribution.png`, `gni_vs_hdi_scatter.png`, `life_expectancy_vs_hdi.png`, `box_plots.png`, `pair_plot.png`, `strip_plot.png`.

### 4. Jinja2 Layout Templates (`templates/`)
* `base.html`: Main shell template.
* `index.html`: Dashboard grid and forms.
* `result.html`: Predicted values card and suggestions.
* `about.html`: Math formulas and coefficients table.
* `404.html`, `500.html`: Custom error overrides.

### 5. Static Assets (`static/`)
* `css/style.css`: Theme control CSS variables, glassmorphic layout tokens, printing style rules.
* `js/script.js`: Syncing sliders, dark mode controls, country metric prefills, LocalStorage cache handlers.

### 6. Tests Package (`tests/`)
* `test_app.py`: Route validation test routines.
* `test_model.py`: Training fit test routines.
