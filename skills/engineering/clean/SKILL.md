---
name: clean
description: Review code for clean naming conventions — descriptive, intention-revealing names. Use when the user invokes /clean or asks for a clean code naming review.
disable-model-invocation: true
---

## Naming

- Use descriptive, intention-revealing names. A variable name should tell you why it exists, what it does, and how it's used.
- Avoid abbreviations and single-letter names outside of tiny loop scopes.
- Use consistent naming conventions across the codebase (e.g., `camelCase` for variables, `PascalCase` for types/classes).
- Name booleans as predicates: `isActive`, `hasPermission`, `shouldRetry`.
- Name functions after what they do, not how they do it.

## Functions

- Keep functions short and focused on a single task. If you need a comment to explain a section, extract it into a well-named function.
- Limit parameters. More than 3 usually means you should pass an object/struct.
- Avoid side effects. A function named `getUser` should not also modify state. If it does, the name should reflect that.
- Prefer pure functions where practical — same inputs, same outputs, no hidden state.
- Return early to avoid deep nesting. Guard clauses up top, happy path below.

## Structure and Organization

- Follow the Single Responsibility Principle at every level: functions, modules, and files should each have one reason to change.
- Group code by feature/domain, not by technical layer, when the codebase is large enough to warrant it.
- Keep files focused. If a file requires extensive scrolling or has multiple unrelated sections, split it.
- Manage dependencies deliberately. Depend on abstractions where volatility is high; depend on concretes where stability is high.

## SOLID Principles

- **Single Responsibility (SRP):** A class or module should have one reason to change. If a class handles both user authentication and email formatting, split it. When you describe what something does and use the word "and," that's a hint.
- **Open/Closed (OCP):** Code should be open for extension but closed for modification. Add new behavior through new code (new classes, new implementations) rather than editing existing, tested code. Polymorphism, strategy patterns, and plugin architectures all serve this.
- **Liskov Substitution (LSP):** Subtypes must be substitutable for their base types without breaking correctness. If a function accepts a base class, any derived class should work without surprises. A classic violation: a `Square` subclass of `Rectangle` that breaks when `setWidth` and `setHeight` are called independently.
- **Interface Segregation (ISP):** Don't force clients to depend on methods they don't use. Prefer small, focused interfaces over large, general-purpose ones. If implementers routinely leave methods as no-ops or throw `NotImplemented`, the interface is too wide.
- **Dependency Inversion (DIP):** High-level modules should not depend on low-level modules — both should depend on abstractions. Your business logic shouldn't import a specific Postgres driver directly; it should depend on a repository interface that a Postgres implementation satisfies. This makes swapping implementations and testing straightforward.

## Error Handling

- Handle errors explicitly. Don't swallow exceptions or ignore error return values.
- Fail fast and fail loudly in development. Provide clear, actionable error messages.
- Use typed/structured errors over raw strings when the language supports it.
- Distinguish between recoverable errors (retry, fallback) and programmer errors (crash, fix the bug).

## Comments and Documentation

- Code should be self-documenting through clear naming and structure. Comments explain _why_, not _what_.
- Delete commented-out code. That's what version control is for.
- Document public APIs, non-obvious design decisions, and known limitations.
- Keep comments maintained. A stale comment is worse than no comment.

## Testing

- Write tests that describe behavior, not implementation. Tests should survive refactors.
- Each test should have a single reason to fail.
- Use descriptive test names that read as specifications: `rejects_expired_tokens`, `returns_empty_list_when_no_results`.
- Avoid testing private internals. Test the public interface.
- Keep tests fast. Slow tests don't get run.

## General Discipline

- Don't repeat yourself, but don't abstract prematurely either. Duplication is cheaper than the wrong abstraction.
- Leave code cleaner than you found it (Boy Scout Rule).
- Prefer immutability and const-correctness by default.
- Optimize for readability first, performance second — unless profiling tells you otherwise.
- Delete dead code. Unused imports, unreachable branches, vestigial functions — remove them.
- Keep diffs small. Small, focused commits and PRs are easier to review, easier to revert, and less likely to introduce bugs.
