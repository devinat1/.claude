---
name: clean
description: Review code for clean naming conventions — descriptive, intention-revealing names. Use when the user invokes /clean or asks for a clean code naming review.
disable-model-invocation: true
---

# Clean Naming

- Use descriptive, intention-revealing names. A variable name should tell you why it exists, what it does, and how it's used.
- Avoid abbreviations and single-letter names outside of tiny loop scopes.
- Use consistent naming conventions across the codebase (e.g., `camelCase` for variables, `PascalCase` for types/classes).
- Name booleans as predicates: `isActive`, `hasPermission`, `shouldRetry`.
- Name functions after what they do, not how they do it.
