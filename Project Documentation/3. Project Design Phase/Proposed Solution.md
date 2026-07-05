# Proposed Solution Document

This document outlines the design and functional characteristics of the proposed Human Development Index (HDI) Predictor system.

---

## 💡 Overview of the Solution

The HDI Predictor is a web-based, machine-learning-powered platform that enables policy analysts, academics, and the public to estimate a country's development index based on key health, education, and income metrics. It offers a fast, interactive simulation sandbox that bypasses manual spreadsheet consolidation.

---

## 🎨 Design Theme & Core UX Aesthetics

1. **Glassmorphism:** Visual elements (cards, headers, sidebars) use translucent backdrops (`backdrop-filter: blur(12px)`) and thin borders (`1px solid rgba(226, 232, 240, 0.8)`) to create depth and modern appeal.
2. **Light / Dark Mode:** Custom CSS variables define colors for both themes. Toggle state is preserved in the browser's local cache.
3. **Responsive Side Layout:** The desktop dashboard features a sticky sidebar. On mobile viewports, the sidebar collapses into a slide-out drawer, optimizing screen space.
4. **Data Visualizations:** Visual correlation heatmaps, pair plots, and strip plots are rendered dynamically under the EDA section, keeping statistical insights close to the calculator.

---

## ⚙️ Core Application Modules

```text
+-------------------+      +-------------------+      +-------------------+
|   Web UI Module   | ---> |  Flask Route Controller | ---> |  Prediction Engine|
| (Jinja2 Templates)|      | (app.py API)      |      | (LinearRegression)|
+-------------------+      +-------------------+      +-------------------+
          ^                          ^                          |
          |                          |                          v
  [Theme Toggle &   ]        [Auth Session &     ]      [Joblib Pickles     ]
  [LocalStorage JS  ]        [Bounds Validation  ]      [hdi_model/scaler   ]
```

1. **Data Pipeline:** Ingests UNDP time-series CSV data, cleans missing entries, and fits a StandardScaler.
2. **Predictive Engine:** Linear Regression model mapping feature standard deviations to estimated HDI values.
3. **Web Server:** Flask app serving authentication checks, metrics endpoints, prediction calculators, and API routers.
4. **Interactive Dashboard:** Form controls with synchronized range sliders, dynamic country auto-fill, and client-side history lists with CSV exports.
