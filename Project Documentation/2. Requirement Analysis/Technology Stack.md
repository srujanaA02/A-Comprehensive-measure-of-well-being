# Technology Stack Specification

This document lists and details the core technologies chosen for the HDI Predictor implementation, justifying their selection based on project constraints.

---

## 🛠 Technology Stack List

| Technology Layer | Chosen Component | Version / Context | Selection Justification |
| :--- | :--- | :--- | :--- |
| **Programming Language** | **Python** | `3.10`+ | Core language for data science and web scripting with massive package ecosystem. |
| **Backend Framework** | **Flask** | `3.0`+ | Lightweight WSGI web framework suited for rapid development and API routing without ORM overhead. |
| **Machine Learning** | **Scikit-Learn** | `1.2`+ | Standard ML library containing efficient implementation of Linear Regression and scaling tools. |
| **Data Manipulation** | **Pandas** | `2.0`+ | Provides powerful DataFrame manipulation routines used for parsing wide-format UNDP datasets. |
| **Scientific Operations** | **NumPy** | `1.24`+ | Drives linear algebra calculations and array standardizations behind ML predictions. |
| **Visualizations** | **Matplotlib** / **Seaborn** | `3.7`+ / `0.12`+ | Generation of high-fidelity EDA plots (correlation matrices, KDE distributions, scatters). |
| **Frontend Framework** | **Bootstrap 5** | `5.3.0` | Provides responsive layout grid system, pre-built utility forms, and buttons. |
| **Icons Library** | **Font Awesome** | `6.4.0` | Comprehensive icons list mapping specific development areas (health, cap, line chart). |
| **Client Scripting** | **Vanilla JS** | ES6 / Native | Lightweight scripting used to control range syncs, theme toggles, and localStorage caching without heavy framework binaries. |
| **Persistence** | **Browser LocalStorage** | HTML5 standard | Eliminates database integration, offering client-side history logs without backend data leaks. |

---

## 🏗 System Runtime Context

* **Development WSGI:** Flask Built-in server (debug mode active for trace logs).
* **Production WSGI Recommendation:** Gunicorn or Waitress.
* **MathJax CDN:** Standard javascript CDN used to render LaTeX calculations (`MathJax-script`) directly in `/about` routes.
