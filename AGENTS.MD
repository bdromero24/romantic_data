# Agents Specification

## 🎯 Purpose
Define strict rules and constraints for any coding agent (Codex) working on this project.

---

## 🔒 HARD CONSTRAINTS (NON-NEGOTIABLE)

1. Do NOT modify files outside the scope of the current task
2. Do NOT rewrite existing modules unless explicitly required
3. Do NOT duplicate logic across files
4. Do NOT introduce unnecessary dependencies
5. Do NOT hardcode credentials or sensitive data
6. Do NOT mix responsibilities between modules
7. Do NOT generate monolithic scripts

---

## 🧱 ARCHITECTURE RULES

- Each module has a single responsibility
- ETL is strictly separated from analysis
- Database logic must exist ONLY in `db/`
- Logging must go ONLY through `logger/`
- Streamlit must NOT contain business logic or show sensitive data when an error ocurr: (database.error(), timeout.error())
- All reusable logic must be inside functions

---

## 🧪 TESTING RULES

- All critical modules must be testable
- Functions must be deterministic
- Avoid side effects when possible
- Use isolated test cases (unit tests)

---

## 🗄️ DATABASE RULES

- Use parameterized queries ONLY
- No string concatenation in SQL
- Use connection abstraction from `db/connection.py`
- Handle exceptions explicitly:
  - ProgrammingError
  - DatabaseError
  - ConnectionError

---

## 🧾 LOGGING RULES

- All errors MUST be logged
- Logging must:
  - Write to `.txt`
  - Insert into PostgreSQL `logs` table
- Include:
  - error_type
  - message
  - timestamp

---

## 🧠 CODE STYLE RULES

- Use type hints
- Use clear, descriptive names
- Prefer small functions
- Avoid deeply nested logic
- Follow PEP8

---

## 📤 OUTPUT RULES (CRITICAL)

Codex must return ONLY:

1. File paths + code
2. Updated `.md` files if required
3. No explanations unless explicitly requested

---

## 🚫 FORBIDDEN ACTIONS

- Adding UI before backend is ready
- Skipping logging in error-prone operations
- Writing queries outside `db/queries.py`
- Mixing ETL and analysis logic
- Ignoring documentation updates

---

## ✅ SUCCESS CRITERIA

- Code runs locally
- Modules are reusable
- Logging works correctly
- DB interactions are safe and parameterized
- Tests can be executed independently