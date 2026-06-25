# Project Context

## 🎯 Objective

Build a modular data analysis application that processes personal conversation data and generates insights using NLP and statistical analysis.

---

## 🧱 Architecture

The system is divided into:

1. ETL Layer
   - Extract raw JSON
   - Normalize structure
   - Load into PostgreSQL

2. Data Layer
   - PostgreSQL stores structured messages
   - Parameterized queries

3. Analysis Layer
   - NLP preprocessing
   - Sentiment analysis
   - Behavioral metrics

4. Presentation Layer
   - Streamlit dashboard

---

## 🧾 Logging System

- Centralized logging
- Outputs:
  - File (.txt)
  - Database (logs table)
- Captures:
  - DB errors
  - ETL errors
  - Runtime errors

---

## 🧪 Testing Strategy

- Unit tests using pytest
- Focus areas:
  - DB connection
  - Logger
  - ETL transformations

---

## ⚙️ Current State

- Project structure defined
- Documentation initialized
- Ready to implement:
  - DB connection
  - Logger system
  - Schema creation

---

## 📌 Constraints

- No business logic in UI
- No SQL outside db module
- No logging outside logger module
- Strict modular design