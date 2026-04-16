
## Aggregate Rules

- Reference other aggregates by identity only. Never hold direct object references to another aggregate; use its ID.
- One aggregate per transaction. A single transaction must only modify one aggregate. Handle cross-aggregate consistency via eventual consistency and domain events.
- The aggregate root is the sole entry point. External objects may only reference the root entity, never internal entities or value objects.
- Enforce invariants within the aggregate boundary. The aggregate is responsible for maintaining its own consistency on every state change.
- Keep aggregates small. Only group entities together when a true transactional invariant requires it.

## Bounded Context Rules

- Each bounded context owns its own ubiquitous language and model. The same real-world concept may have different representations in different contexts.
- Models must not leak across context boundaries. Use anti-corruption layers, published languages, or shared kernels to communicate between contexts.
- A single team should own a bounded context.

## Domain Modeling Rules

- Model the domain, not the database. The domain model drives design; the persistence schema follows.
- Ubiquitous language is non-negotiable. Code, conversation, and documentation must use the same domain terms. If the language changes, the code changes.
- Entities have identity; value objects do not. Value objects must be immutable and compared by their attributes.
- Domain logic belongs in the domain layer. Never place domain logic in application services, controllers, or infrastructure. Avoid anemic models where entities are data holders and services contain all behavior.
- Repositories abstract persistence. The domain layer must not know about databases, ORMs, or query mechanics. Repositories accept and return aggregates.
- Factories handle complex creation. When constructing an aggregate involves non-trivial logic, encapsulate it in a factory.
- Domain events capture side effects. When something in one aggregate matters to other parts of the system, express it as an explicit domain event rather than coupling aggregates together.
