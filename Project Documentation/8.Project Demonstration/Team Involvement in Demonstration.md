# Team Involvement in Demonstration

This document maps role responsibilities and tasks during the project demonstration and final review phase.

---

## 👥 Roles & Demonstration Assignments

| S.No | Team Role | Assigned Member | Demo Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | **Project Presenter** | Lead Developer | Introduces the problem statement, explains the importance of HDI simulations, and drives the walkthrough of the login and dashboard features. |
| 2 | **Technical Explainer** | ML Engineer | Details the training pipeline (`train_model.py`), explaining data preprocessing (melting), standard scaling, and the regression coefficients on the `/about` route. |
| 3 | **Scenarios Driver** | UI Engineer | Executes the three scenarios (Very High, Medium, and Low HDI predictions), demonstrating range slider synchronizations and pre-fill capabilities. |
| 4 | **QA Evaluator** | QA Tester | Verifies history cache saving, triggers the CSV downloads, and answers questions regarding validation boundary checks. |

---

## 📈 Demo Day Guidelines

1. **Environment Verification:** Before demonstrating, run the automated test suite `python -m unittest discover -s tests` to verify all components compile correctly.
2. **Server Check:** Launch the Flask server in clean port context: `python app.py`. Ensure database stats caches load successfully on startup.
3. **Data Logs:** Keep prediction histories clear before the presentation, allowing stakeholders to see logs populate from scratch.
