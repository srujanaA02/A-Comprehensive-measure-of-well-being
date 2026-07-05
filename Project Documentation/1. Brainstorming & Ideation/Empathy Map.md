# Empathy Map

Understanding our core user persona helps us build a customer-centric solution. This empathy map focuses on the **Policy Analyst** persona.

---

## 👤 Persona: Elena Vance (Development Policy Analyst)

```text
               +----------------------------------+----------------------------------+
               |               SAYS               |              THINKS              |
               |                                  |                                  |
               | * "I need to run real-time       | * "I wonder if increasing secondary |
               |   simulations for our education  |   schooling yields more HDI gain |
               |   reforms before presenting."    |   than increasing health funding?" |
               | * "Manual data cleaning in Excel | * "Static data charts from 2021  |
               |   takes up 60% of my workday."   |   don't help predict future      |
               | * "The tool must look modern and |   development goals."            |
               |   be accessible on my tablet."   | * "I hope the prediction model   |
               |                                  |   is mathematically explainable."|
               +----------------------------------+----------------------------------+
               |                                PERSONA:                             |
               |                              Elena Vance                            |
               +----------------------------------+----------------------------------+
               |               DOES               |              FEELS               |
               |                                  |                                  |
               | * Consolidates annual UN reports | * Overwhelmed by scattered, wide |
               |   manually into local files.     |   datasets in varying formats.   |
               | * Presents development proposals | * Skeptical of opaque "black-box"|
               |   to regional decision makers.   |   ML predictions.                |
               | * Formulates action items based  | * Relieved when finding clean,   |
               |   on weakest regional indexes.   |   explainable, visual dashboards.|
               +----------------------------------+----------------------------------+
```

---

## 🎯 Design Requirements Driven by Elena's Empathy Map
1. **Interactive Simulation:** Built a reactive input form where slider actions dynamically update indicator values in real-time.
2. **Explainable ML Model:** Provided an `/about` route demonstrating the exact mathematical normalization formulas and the fitted feature weights of the model.
3. **Data Caching & Export:** Configured client LocalStorage to store prediction histories, avoiding database load times, and added a quick CSV/JSON exporter.
