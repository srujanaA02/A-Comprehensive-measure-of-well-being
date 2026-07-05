# Data Flow Diagram (DFD)

This document visualizes the movement of data throughout the HDI Predictor application, mapping inputs from the user interface, through the Flask routing, into the machine learning predictors, and back to the client templates.

---

## 📈 DFD Level 0 (Context Diagram)

```mermaid
graph LR
    User([User Web Browser])
    System[[HDI Predictor System]]
    CSV[("hdi_processed.csv")]
    
    User --> |1. Prefill Query| System
    System --> |2. Fetch Country Rows| CSV
    CSV --> |3. Country Metrics JSON| System
    System --> |4. Render Option Values| User
    
    User --> |5. Submit Indicator Form| System
    System --> |6. Process ML Model & Calc| System
    System --> |7. Predicted Score & PDF Page| User
```

---

## 📉 DFD Level 1 (Process Diagram)

```mermaid
flowchart TD
    User([User Web Browser])
    
    subgraph "Process 1.0: Ingestion & Training (Off-line)"
        P11["Download raw series"]
        P12["Clean & Melt data"]
        P13["Fit Regression Model"]
        P14["Serialize Pickles"]
    end
    
    subgraph "Process 2.0: Flask Web Controller (On-line)"
        P21["Auth session check"]
        P22["Load ML assets"]
        P23["Validate Input Bounds"]
        P24["Standardize Features"]
        P25["Predict HDI Score"]
        P26["Render Result Template"]
    end
    
    subgraph "Process 3.0: Client History Cache"
        P31["Update LocalStorage array"]
        P32["Render History Table"]
        P33["Export CSV Stream"]
    end
    
    %% Ingestion Links
    UNDP[("UNDP Online CSV")] --> |Raw records| P11
    P11 --> |hdi_raw.csv| P12
    P12 --> |hdi_processed.csv| P13
    P13 --> |StandardScaler & Weights| P14
    P14 --> |scaler.pkl & hdi_model.pkl| P22
    
    %% User Request Links
    User --> |HTTP GET /| P21
    P21 --> |Check session| P22
    P22 --> |Prefilled country dropdown| User
    
    User --> |HTTP POST /predict| P23
    P23 --> |Valid Float Features| P24
    P24 --> |Transformed Vector| P25
    P25 --> |Clamped Prediction| P26
    P26 --> |Render HTML Result| User
    
    %% Browser script updates
    User --> |Save Prediction| P31
    P31 --> |localStorage array| P32
    P32 --> |Export history event| P33
    P33 --> |Trigger Download| User
```
