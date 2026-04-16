
Follow these rules when writing and reviewing code. They are drawn from Robert C. Martin's _Clean Code_, _Clean Architecture_, and the SOLID principles.

## Core Philosophy

Code is read far more often than it is written. Optimize for readability above almost everything else. First drafts are messy — the craft is in the rewriting.

Leave the code cleaner than you found it (Boy Scout Rule). Every commit should improve the codebase slightly.

## Functions

- Keep functions small. Under 20 lines is a good target.
- A function should do one thing, do it well, and do it only.
- Operate at one level of abstraction per function. Don't mix high-level policy with low-level string parsing in the same function.
- Minimize arguments. Zero is ideal, one or two is fine, three is suspicious, more than three needs strong justification. If you need many parameters, consider grouping them into an object.
- Don't use flag arguments (booleans that make a function do two different things).
- Prefer exceptions over return codes.
- Extract until every function reads like a single logical step.

## Naming

- Names should reveal intent. `elapsedTimeInDays` over `d`. `isEligibleForOvertime()` over `check()`.
- Classes get noun names (`Employee`, `OrderRepository`). Functions get verb names (`calculatePay`, `sendEmail`).
- Don't be clever or cute. `kill()` over `whack()`.
- Don't use encodings or prefixes like Hungarian notation (`strName`, `m_count`).
- Don't make the reader mentally translate names. `r` doesn't mean anything.
- Use consistent vocabulary. Pick one word per concept and stick with it (`fetch`, `retrieve`, and `get` should not coexist for the same idea).

## Comments

- A comment is a failure to express yourself in code. If you need one, first try rewriting the code so it doesn't need one.
- Acceptable comments: legal headers, TODOs, warnings about consequences, clarification of intent when the code truly cannot be made clearer.
- Never commit commented-out code. Delete it. Version control remembers.
- Don't write redundant comments that just restate what the code already says.

## Error Handling

- Use exceptions, not return codes.
- Write try-catch-finally blocks first when writing code that can fail.
- Don't return `null`. Return empty collections, Optional, or a sensible default. Returning `null` pushes null-checking onto every caller.
- Don't pass `null` as a function argument.
- Create informative error messages that provide context about what failed and why.

## Classes and Objects

- Classes should be small in responsibility, not just line count.
- Single Responsibility Principle: a class should have one reason to change, meaning one stakeholder whose needs could cause modification.
- High cohesion: methods should use most of the class's instance variables. If a subset of methods only touches a subset of fields, that's a new class waiting to be extracted.
- Prefer composition over inheritance when practical.

## SOLID Principles

### Single Responsibility (SRP)

A class has one reason to change. "Reason" means one actor or stakeholder. If two different departments could request changes to the same class, split it.

### Open/Closed (OCP)

Open for extension, closed for modification. Add new behavior by adding new code (new classes, new implementations), not by editing existing code. This is where polymorphism pays off.

### Liskov Substitution (LSP)

Subtypes must be substitutable for their base types without breaking program correctness. If a subclass surprises callers of the base class, the hierarchy is wrong.

### Interface Segregation (ISP)

No client should be forced to depend on methods it does not use. Prefer small, focused interfaces over large, general-purpose ones.

### Dependency Inversion (DIP)

High-level modules should not depend on low-level modules. Both should depend on abstractions. Inject dependencies (usually via constructor injection) rather than creating them internally.

## Dependency Injection

- Depend on abstractions (interfaces), not concretions (implementations).
- Pass dependencies in through constructors. Don't have classes instantiate their own collaborators.
- DI frameworks are tools, not architecture. Constructor injection is usually sufficient. Don't let Spring, Guice, or similar frameworks dictate your design.
- Dependencies should point inward: business rules at the center know nothing about databases, UI, or frameworks on the outside.

## Switch Statements

- Switch statements on type codes are a code smell. They tend to get duplicated across the codebase and violate OCP.
- Replace with polymorphism: each case becomes a subclass that implements the behavior.
- A switch is tolerable if it appears exactly once, lives in a factory, and is used to create polymorphic objects.

## Tests

- Follow TDD's three laws:
    1. Don't write production code until you have a failing test.
    2. Don't write more of a test than is sufficient to fail.
    3. Don't write more production code than is sufficient to pass the test.
- Tests should be F.I.R.S.T.: Fast, Independent, Repeatable, Self-validating, Timely.
- Keep tests clean and readable. Test code is as important as production code.
- One concept per test. Aim for one logical assertion per test (not necessarily one `assert` call, but one idea being verified).
- Tests are documentation. A reader should understand the production code's behavior by reading the tests.

## Formatting

- Files should read like newspaper articles: headline (class name), synopsis (high-level public methods), then details (private methods, helpers) as you scroll down.
- Keep related code vertically close. A function and the functions it calls should be near each other.
- Be consistent with your team's formatting conventions. Consistency matters more than any individual rule.
- Keep lines short. If you have to scroll horizontally, the line is too long.

## Boundaries

- Wrap third-party APIs in your own thin abstraction layer. Don't let external types leak across your codebase.
- This lets you swap implementations, control the interface, and isolate breakage when the third party changes.
- Write learning tests for third-party code to verify your understanding and detect breaking changes on upgrades.

## Law of Demeter

- A method should only call methods on: its own object, its parameters, objects it creates, and its direct collaborators.
- Avoid train wrecks: `a.getB().getC().doThing()` exposes too much internal structure.
- "Tell, don't ask." Tell objects what to do rather than interrogating their internals.

## DRY (Don't Repeat Yourself)

- Duplication is the primary enemy of clean code. Every piece of knowledge should have a single, unambiguous representation.
- If you find yourself copying and pasting, extract the common logic.
- This applies to logic, not just literal text. Two blocks that look different but encode the same business rule are still duplication.

## Pragmatism

These are guidelines, not rigid laws. They matter most when codebases are large, teams are big, and requirements are evolving. For a small script, prototype, or spike, strict adherence is counterproductive. Use judgment.
