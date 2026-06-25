# Agents Specification

## Purpose

Define strict rules and constraints for any coding agent working on this project.

## Hard Constraints

1. Do NOT modify files outside the scope of the current task.
2. Do NOT rewrite existing modules unless explicitly required.
3. Do NOT duplicate logic across files.
4. Do NOT introduce unnecessary dependencies.
5. Do NOT hardcode credentials or sensitive data.
6. Do NOT mix responsibilities between modules.
7. Do NOT generate monolithic scripts.

## Architecture Rules

- Each module has a single responsibility.
- ETL is strictly separated from analysis.
- Database logic must exist ONLY in `db/`.
- Logging must go ONLY through `logger/`.
- Streamlit must NOT contain business logic or show sensitive data when an error occurs.
- All reusable logic must be inside functions.

## Testing Rules

- All critical modules must be testable.
- Functions must be deterministic.
- Avoid side effects when possible.
- Use isolated test cases.

## Database Rules

- Use parameterized queries ONLY.
- No string concatenation in SQL.
- Use connection abstraction from `db/connection.py`.
- Handle `ProgrammingError`, `DatabaseError`, and `ConnectionError` explicitly.

## Logging Rules

- All errors MUST be logged.
- Logging must write to `.txt` and insert into PostgreSQL `logs`.
- Include `error_type`, `message`, and `timestamp`.
