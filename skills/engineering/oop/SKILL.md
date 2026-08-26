---
name: oop
description: Review code against principles from Elegant Objects by Yegor Bugayenko. Use when the user invokes /oop or asks for an elegant objects review.
disable-model-invocation: true
---

Based on the principles from _Elegant Objects_ by Yegor Bugayenko.

## Consequential advice

Before recommending a consequential design change, follow the `Advice gate`
in `dissenter`; report evidence-only findings directly.
When the gate applies, first say that you are using `/dissenter` and why.

## Objects

- **Do** treat objects as living organisms with behavior.
- **Don't** use objects as passive data bags that external code manipulates.
- **Do** make objects immutable by default. Use `final`/`readonly` fields.
- **Don't** create mutable state unless absolutely necessary.
- **Do** make objects fully formed at construction time. Everything they need comes through the constructor.
- **Don't** allow objects to exist in a half-initialized or invalid state.

## Naming

- **Do** name classes as nouns representing what they _are_ (`Invoice`, `HttpRequest`, `ParsedFile`).
- **Don't** use "-er" names (`Manager`, `Controller`, `Helper`, `Validator`, `Processor`). These indicate procedural thinking.

## Constructors

- **Do** use constructors as the sole way to configure and initialize objects.
- **Don't** use static factory methods, builders, or setter-based initialization.
- **Do** keep constructors simple — store dependencies, don't do heavy work.

## Getters and Setters

- **Don't** expose internal state through getters.
- **Don't** allow external mutation through setters.
- **Do** provide behavior methods instead. If you're calling a getter to do something with the value, that logic belongs on the object itself.
- **Do** follow "tell, don't ask" — tell the object what you need, don't ask for its data.

## Static Methods

- **Don't** use static methods. They are procedural code in OOP disguise.
- **Don't** create utility classes (`StringUtils`, `FileUtils`, `DateUtils`). These are junk drawers.
- **Do** use object instances with interfaces so dependencies can be swapped, mocked, and composed.

## NULL

- **Don't** return `null` from methods. It pushes error handling onto every caller and propagates silently.
- **Do** fail fast — throw a meaningful exception if something is genuinely wrong.
- **Do** use Null Objects that implement the interface with safe no-op behavior.
- **Do** return empty collections instead of `null` when a result set may be empty.

## Error Handling

- **Do** fail fast and loud. Throw exceptions with clear messages.
- **Don't** return error codes, special sentinel values, or `-1`.
- **Don't** swallow exceptions silently.
- **Do** keep exception handling close to where the error originates.

## Class Design

- **Do** keep classes small and focused. Each class should have a single clear responsibility.
- **Don't** create deep inheritance hierarchies. Prefer composition and decorators.
- **Do** use decorators to add behavior instead of utility classes or inheritance.
- **Do** program to interfaces, not implementations.

## Encapsulation

- **Do** hide all internal representation. Callers should never know how an object stores its data.
- **Don't** break encapsulation for convenience (serialization, logging, debugging). Provide proper behavioral methods instead.
- **Do** make it possible to change internal representation without affecting callers.

## General

- **Don't** write code that is clever. Write code that is simple and readable.
- **Do** prefer many small objects composed together over few large objects doing everything.
- **Don't** use reflection, annotations, or runtime magic to wire things together.
- **Do** make dependencies explicit. If a class needs something, it should be in the constructor.
