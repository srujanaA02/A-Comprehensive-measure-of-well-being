# Solution Architecture Specification

This document details the software architecture layers and interaction protocols behind our HDI Predictor system.

---

## 🏛 Solution Layers Diagram

```mermaid
graph TD
    subgraph "Client Layer (Web Browser)"
        UI["Bootstrap 5 View (HTML/CSS)"]
        Script["Vanilla JS Engine (script.js)"]
        Cache[("LocalStorage Caching")]
    end
    
    subgraph "Web Application Layer (Flask)"
        Server["Flask App Instance (app.py)"]
        Auth["Session Auth middleware"]
        Val["Bounds Validator"]
        API["Country Metrics API"]
    end
    
    subgraph "Machine Learning Engine (Scikit-Learn)"
        Scaler["StandardScaler (scaler.pkl)"]
        Reg["LinearRegression (hdi_model.pkl)"]
    end
    
    subgraph "Data Storage Layer"
        TidyCSV[("hdi_processed.csv")]
    end
    
    %% Client Interactions
    UI --> |Theme Switch / History log| Script
    Script <--> |Local state| Cache
    UI --> |1. POST Form /predict| Server
    UI --> |2. GET Prefill metrics| API
    
    %% Server Controller Interactions
    Server --> Auth
    Auth --> |Authorized request| Val
    API --> |Read lookup values| TidyCSV
    
    %% ML processing
    Val --> |Feature array| Scaler
    Scaler --> |Scaled vectors| Reg
    Reg --> |Estimate score| Server
    Server --> |3. Render Result Page| UI
```

---

## 🔗 Architecture Component Descriptions

1. **Authentication Session Guard:** Intercepts requests using `app.before_request`. Validates if `session['logged_in']` is active. Redirects to `/login` if unauthenticated.
2. **Bounds Validator:** Checks incoming query features (Life Expectancy, Schooling, GNI) against predefined ranges. Rejects out-of-bounds metrics with HTTP 400.
3. **ML Pickles Pipeline:**
   * `scaler.pkl`: Restores mean and variance offsets from the training dataset.
   * `hdi_model.pkl`: Houses the weights matrix, multiplying standardized vectors to predict final index scores.
4. **Local History Database:** JavaScript-controlled LocalStorage caching. Encapsulates predictions as JSON dictionaries and appends them to a list, avoiding SQL database setups.
