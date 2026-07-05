# Scalability & Future Scope Plan

This document details the roadmap for expanding the feature set, modeling architecture, and deployment scalability of the HDI Predictor.

---

## 📈 1. Feature Set Expansion

1. **Gender Inequality Index (GII) Predictor:**
   * Integrate gender-disaggregated indicators (maternal mortality, adolescent birth rates, parliamentary seats share, educational attainment).
   * Predict GII alongside HDI to offer a multi-dimensional picture of development equity.
2. **Multidimensional Poverty Index (MPI) Calculator:**
   * Accept deprivation indicators across health (nutrition, child mortality), education (school enrollment), and standard of living (cooking fuel, sanitation, water, assets).
   * Classify severe poverty segments dynamically.

---

## 🤖 2. Advanced Predictive Modeling

1. **Non-Linear Models (Random Forests & Gradient Boosting):**
   * While Linear Regression performs exceptionally well, random forest regressors can model complex joint feature distributions, reducing error offsets.
2. **Time-Series Forecasting (ARIMA / LSTM):**
   * Incorporate historic time-series data to predict country development paths (e.g. estimating a country's HDI score for 2030 based on current growth trends).

---

## ☁️ 3. Cloud Integration & Scalability

1. **SQL Database Migration:**
   * Replace LocalStorage caching with a centralized relational database (e.g. **PostgreSQL** or **SQLite**) managed via **SQLAlchemy**.
   * Secure user accounts with database hashed passwords (`bcrypt`).
2. **Dockerization:**
   * Package the application in a lightweight **Docker** container to run consistently on AWS, GCP, or Azure:
     ```dockerfile
     FROM python:3.11-slim
     WORKDIR /app
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY . .
     EXPOSE 5000
     CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
     ```
