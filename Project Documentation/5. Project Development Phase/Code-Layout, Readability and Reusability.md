# Code-Layout, Readability, and Reusability Report

This document reviews our codebase structure, coding conventions, readability metrics, and modular design.

---

## 📐 1. Code-Layout Conventions

We adhere to the **PEP 8 style guide** for Python development:
* **Naming Conventions:**
  * Variables and functions: lowercase with underscores (`life_expectancy`, `load_ml_resources`).
  * Class names: PascalCase (`Config`).
  * Constants: uppercase with underscores (`BASE_DIR`, `RAW_DATA_URL`).
* **Indentation:** 4 spaces (no tabs).
* **Maximum Line Length:** Capped at 80-120 characters for clean terminal viewports.
* **Blank Lines:** Two blank lines surrounding class functions and module-level code.

---

## 📖 2. Readability & Code Documentation

* **Docstrings:** All python functions include detailed multi-line docstrings detailing the purpose, arguments, and return types.
* **Logging:** Avoid using raw `print()` statements for production logging. Built-in `logging` module is configured in `app.py`, writing formatted event traces to standard stdout and a persistent `app.log` file.
* **Self-documenting variables:** Variables are explicitly named (e.g. `expected_years_schooling` instead of `eys`), enhancing code transparency.

---

## 🔄 3. Reusability Design Patterns

1. **Jinja2 Templates Inheritance:**
   * [`base.html`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/templates/base.html) serves as the parent layout structure containing the dark mode toggle scripts, mobile navigation responsive drawer, loading screen, and headers.
   * Target views ([`index.html`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/templates/index.html), [`result.html`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/templates/result.html), [`about.html`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/templates/about.html)) extend `base.html`, overriding only their specific content blocks.
2. **Unified Configuration Class:**
   * [`config.py`](file:///C:/Users/User/.gemini/antigravity/scratch/hdi_predictor/config.py) isolates folder directories, dataset links, and serialization paths in a single class imported across script pipelines.
3. **Reusable CSS Classes:**
   * Custom helper variables (`--teal-primary`, `--bg-app`) are defined in `:root`. Modern design tokens like glassmorphism card wrappers (`.glass-card`, `.glass-panel`) are written once and used globally across templates.
