# Demonstration of Proposed Features

This document outlines the demo flow, listing our main features, demonstrating how to show them in action, and highlighting their design highlights.

---

## 🖥 Demo Checklist of Implemented Features

### Feature 1: Session-Based Authentication
* **How to demonstrate:** 
  1. Open a private window and go to `http://127.0.0.1:5000/`. Observe the automatic redirect to `/login`.
  2. Click "Sign In" using the pre-filled demo credentials (`admin` / `admin123`).
  3. Verify access to the dashboard.
* **Design Highlight:** Standalone glassmorphic login card with dynamic theme sync.

### Feature 2: Country Metric Prefill
* **How to demonstrate:**
  1. Select "Germany" or "India" from the Country Reference dropdown.
  2. Observe that inputs for Life Expectancy, Expected Schooling, Mean Schooling, and GNI per Capita are instantly filled.
* **Design Highlight:** AJAX query endpoint `/api/country/<name>` dynamically updates form values and range sliders in real-time.

### Feature 3: Interactive Simulation Sandbox
* **How to demonstrate:**
  1. Drag the "Life Expectancy" slider or the "GNI per Capita" slider on the dashboard.
  2. Observe that the numeric inputs and GNI text labels sync instantly.
* **Design Highlight:** Real-time bi-directional input range listeners.

### Feature 4: Model Prediction & suggestions
* **How to demonstrate:**
  1. Submit the form with custom values (e.g. Life Expectancy = 82, Schooling = 16/13, GNI = 55,000).
  2. Review the `/predict` result page displaying a predicted score (e.g., `0.925`) and category tier.
  3. Observe the customized dimension progress bars and policy recommendations.
* **Design Highlight:** Dynamic category classification engine and target deficiency analyzer.

### Feature 5: Prediction History & CSV Exporters
* **How to demonstrate:**
  1. Perform multiple predictions (e.g., Scenario 1, 2, and 3).
  2. Navigate back to the Dashboard and scroll to the bottom.
  3. Verify that all past queries are logged in the history table.
  4. Click "Export" to download a CSV of the history logs.
* **Design Highlight:** DB-free client storage using LocalStorage.
