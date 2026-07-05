# Project Planning Document

This document lists our development roadmap, tasks, milestones, resource assignments, and task states.

---

## 📅 Project Development Schedule

| Task ID | Task Category | Task Description | Assigned Resource | Start Date | End Date | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-101** | Infrastructure | Set up folders (`static/`, `templates/`, `dataset/`, `models/`), virtual environment, and configurations. | DevOps Engineer | 15 March 2026 | 16 March 2026 | **Completed** |
| **T-102** | Data Pipeline | Write `train_model.py` to download UNDP datasets, melt wide columns, and clean entries. | ML Engineer | 17 March 2026 | 19 March 2026 | **Completed** |
| **T-103** | Model Fitting | Train Linear Regression model, evaluate metrics (MAE, RMSE, R²), and serialize pickles. | ML Engineer | 20 March 2026 | 21 March 2026 | **Completed** |
| **T-104** | Backend API | Write Flask routes (Dashboard, Predict, About, Login/Logout, error pages) and validation checks. | Backend Developer | 22 March 2026 | 25 March 2026 | **Completed** |
| **T-105** | UI Design | Build Bootstrap 5 layouts, custom glassmorphism styles, responsive grid sidebar, and Light/Dark toggling. | UI Designer | 26 March 2026 | 28 March 2026 | **Completed** |
| **T-106** | Client Logic | Implement range slider syncs, country prefill API fetch, and LocalStorage history exports. | UI Designer | 29 March 2026 | 30 March 2026 | **Completed** |
| **T-107** | Unit Testing | Write route tests and model preprocessing tests, verify status codes and range limits. | QA Engineer | 31 March 2026 | 01 April 2026 | **Completed** |
| **T-108** | Verification | Verify app end-to-end (login, simulation, result suggestions, PDF exports). | Team | 02 April 2026 | 03 April 2026 | **Completed** |

---

## 🎯 Key Project Milestones

1. **Milestone 1: Data Pipeline Completion (19 March 2026)**
   * Clean panel dataset generated and saved. Fallback synthetic engine verified.
2. **Milestone 2: Model Inception (21 March 2026)**
   * Linear regression weights serialized. Model achieves $R^2 \ge 99\%$ accuracy.
3. **Milestone 3: Web Dashboard Integration (30 March 2026)**
   * Responsive layout with glassmorphic cards, login page, and LocalStorage caching active.
4. **Milestone 4: Delivery Ready (03 April 2026)**
   * Unit tests passing. Project documentation, diagrams, and deployment guides completed.
