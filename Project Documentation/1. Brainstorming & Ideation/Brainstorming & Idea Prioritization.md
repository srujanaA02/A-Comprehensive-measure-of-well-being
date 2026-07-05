# Brainstorming & Idea Prioritization Template

This document tracks our design thinking lifecycle, from listing candidate ideas to evaluating feasibility and selecting our final implementation architecture.

---

## 💡 Step 1: Brainstorm and Idea Listing

| S.No | Team Member | Idea / Suggestion | Category | Group No. |
| :--- | :--- | :--- | :--- | :--- |
| 1 | AI Engineer | Build an interactive Flask Web UI with custom styling and light/dark theme toggle | Web Interface | Group 1 |
| 2 | ML Engineer | Train a multi-variate Linear Regression model on UNDP indicators using Scikit-Learn | Machine Learning | Group 2 |
| 3 | AI Engineer | Add browser-caching (`localStorage`) to save prediction history locally without a DB | Caching / Storage | Group 3 |
| 4 | ML Engineer | Use deep neural networks (PyTorch) to predict non-linear HDI composite indexes | Machine Learning | Group 2 |
| 5 | UI Designer | Build visual EDA panels containing correlation maps and GNI scatter plots directly in UI | Visualizations | Group 4 |
| 6 | QA Engineer | Write unit tests verifying input validation ranges and Flask routes response codes | Testing | Group 5 |

---

## 📈 Step 2: Idea Prioritization

| Group No. | Final Idea | Feasibility (High/Medium/Low) | Importance (High/Medium/Low) | Priority | Selected (Yes/No) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Group 1** | Responsive Flask dashboard with custom stylesheet and Dark Mode | **High** (Flask provides lightweight server routes; Bootstrap ensures styling grids) | **High** (Ensures professional UX and cross-device responsiveness) | **1** | **Yes** |
| **Group 2** | Linear Regression model trained on melted UNDP panel data | **High** (Scikit-learn features standard fit routines; coefficients map directly to indices) | **High** (Driving core prediction functionality) | **1** | **Yes** |
| **Group 2** | Neural Networks predictor | **Medium** (Higher compilation overhead; potential overfitting for tabular datasets) | **Medium** (Regression is simpler and highly interpretable) | **3** | **No** (Linear Reg achieves 99.4% $R^2$) |
| **Group 3** | LocalStorage history caching with CSV export capability | **High** (Simple browser-side JS API; zero database setup requirements) | **High** (Supports quick data tracking and user convenience) | **2** | **Yes** |
| **Group 4** | Matplotlib/Seaborn EDA plots generated and rendered in UI tabs | **High** (Visual assets compiled during model training) | **High** (Provides crucial model insights for researchers) | **2** | **Yes** |
| **Group 5** | Unittest automated testing suite | **High** (Standard Python `unittest` library integration) | **High** (Ensures regression-free backend routes and validation bounds) | **1** | **Yes** |
