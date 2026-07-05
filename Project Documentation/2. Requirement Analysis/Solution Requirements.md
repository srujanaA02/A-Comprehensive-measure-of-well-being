# Solution Requirements Document

This document lists the system requirements (both functional and non-functional) for our HDI Predictor web application.

---

## ⚙️ 1. Functional Requirements

### FR-1: Authentication & Access
* The system **must** restrict dashboard access to authenticated users.
* Unauthenticated requests **must** be redirected to `/login`.
* Standard pre-filled credentials (`admin` / `admin123`) **must** be supported for easy demo purposes.
* A logout route `/logout` **must** clear active sessions.

### FR-2: Machine Learning Prediction
* The system **must** accept four development indicators:
  1. Life Expectancy (20.0 to 100.0 years)
  2. Expected Years of Schooling (0.0 to 25.0 years)
  3. Mean Years of Schooling (0.0 to 20.0 years)
  4. Gross National Income (GNI) Per Capita ($100 to $150,000 PPP)
* The backend **must** validate bounds, data types, and logical conflicts (e.g. Mean Schooling > Expected Schooling) before prediction.
* The system **must** output an estimated HDI score between $0.000$ and $1.000$ and classify it into standard UN tiers (Very High, High, Medium, Low).

### FR-3: User Interface & Dashboards
* The dashboard **must** display summary metrics of the training dataset.
* The frontend **must** synchronize numeric form inputs with range sliders.
* Selecting a country from the dropdown **must** trigger an API query and prefill the form.
* Tabbed components **must** display EDA visualizations (Correlation matrix, distributions, income scatter).

### FR-4: History Cache & Exporters
* Prediction queries **must** save in local browser storage (`localStorage`).
* The dashboard **must** render a table showing prediction history.
* The system **must** export prediction history as a CSV file and download individual results as JSON.

---

## 🛡 2. Non-Functional Requirements

### NFR-1: Responsiveness & UX
* The UI **must** be fully responsive, scaling properly from desktop down to mobile viewports ($360\text{px}$).
* The style **must** support light and dark modes, saving preference in local cache.
* Interface **must** follow modern glassmorphic cues (blur filters, soft borders, radial gradients).

### NFR-2: Performance & Scalability
* The page load time **should** be under 1.5 seconds.
* Predict API response latency **must** be under $100\text{ms}$.
* The model training pipeline **must** support automated fallback to high-quality synthetic generation if external UNDP downloads fail.

### NFR-3: Testability
* The codebase **must** achieve a high coverage test suite checking ML predictions, validations, and server route codes.
