---
name: scale
description: Analyze branch code for scale limits, upgrade paths, system design diagrams, and learning resources. Use when the user invokes /scale.
disable-model-invocation: true
---

## Consequential advice

Before recommending an upgrade path, technology choice, or learning plan,
follow the `Advice gate` in `dissenter` and wait for the user's choice.
When the gate applies, first say that you are using `/dissenter` and why.

For my code from /branch, tell me:
- What is the scale that my code supports? (how many users), and exactly at which scale will the code break?
- What are the ways I can support a higher scale? (order from low scale to highest (google level) scale).
What are the technologies needed to reach that scale, and draw a system design diagram of how they would work. 
- Provide links to documentation and assignments that I can partake in myself, such as from MIT open courseware, to learn about the gaps in my system when it comes to scale.
- Follow practices from the book titled domain driven design.

After the complete analysis, append the `scale` completion suggestions from
[skill connections](../../../docs/skill-connections.md).
