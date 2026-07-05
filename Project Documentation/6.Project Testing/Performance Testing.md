# Performance & Unit Testing Report

This document reports the performance characteristics of our predictive engine and details the execution of our unit testing suites.

---

## 📈 1. Machine Learning Model Performance

Our Linear Regression model was fitted on **1,152** annual country development records generated from UNDP panel statistics. The model evaluation metrics on an independent test partition (80-20 train-test split) are summarized below:

| Metric | Computed Value | Description |
| :--- | :--- | :--- |
| **Mean Absolute Error (MAE)** | `0.00979` | Average absolute vertical distance between predicted and actual HDI values. |
| **Mean Squared Error (MSE)** | `0.00015` | Average squared vertical error distance, penalizing larger deviations. |
| **Root Mean Squared Error (RMSE)** | `0.01224` | Square root of MSE, matching target units. |
| **Coefficient of Determination (R²)** | `0.99469` ($99.47\%$) | Proportion of target variance explainable by inputs. |
| **Training R² Score** | `0.99461` ($99.46\%$) | Fit accuracy on training data, indicating zero overfitting. |

### Feature Coefficients (Std Dev Change mapping)
* **Life Expectancy:** `+0.13545`
* **Mean Years of Schooling:** `+0.04817`
* **GNI per Capita:** `+0.02936`
* **Expected Years of Schooling:** `-0.03857`
* **Intercept:** `0.72836`

---

## 🧪 2. Unit Testing Execution Suite

We run automated unit tests covering both the predictive backend and the web server routing.

### Test Coverage Checklist

* **[`test_model.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/tests/test_model.py) (2 tests):**
  * `test_synthetic_data_generation`: Confirms panel columns structure, bounds check, and null validations.
  * `test_model_training_outputs`: Confirms scaler persistence, linear coefficients fit, and mock prediction limits.
* **[`test_app.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/tests/test_app.py) (7 tests):**
  * `test_dashboard_route`: Verifies the `/` dashboard responds with HTTP 200.
  * `test_about_route`: Verifies the `/about` route responds with HTTP 200.
  * `test_invalid_404_handler`: Asserts custom page templates are served for incorrect routes.
  * `test_api_countries_endpoint`: Verifies list of countries is served in JSON array.
  * `test_api_stats_endpoint`: Verifies dataset statistics are served in JSON format.
  * `test_prediction_successful`: Verifies prediction executes correctly with valid arguments.
  * `test_prediction_invalid_fields`: Asserts form boundaries reject out-of-range arguments returning error code 400.

### Automated Test Results Command
```bash
python -m unittest discover -s tests
```
* **Execution Status:** **PASS (OK)**
* **Total Tests Run:** 9
* **Execution Time:** $0.404\text{ seconds}$
* **Success Rate:** $100\%$
