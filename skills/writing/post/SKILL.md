---
name: post
description: Use when the user asks to draft, make, schedule, queue, or publish social posts from the current conversation, blog post, article, launch note, or existing post context, especially for X/Twitter and LinkedIn through Postiz.
---

# Post

Draft platform-specific social copy and schedule it through Postiz only after explicit approval.

**REQUIRED SUB-SKILL:** Use `postiz` before any Postiz CLI calls.

## Workflow

1. **Find the source context**
   - Use the current conversation first.
   - Infer a blog/article URL from recent context when available; show it in the preview.
   - If the source is unclear, ask one question before drafting.

2. **Draft both platform versions**
   - X/Twitter: under 280 characters including the URL text. Count before previewing.
   - LinkedIn: short professional post, a bit longer, with clear paragraphs and a practical takeaway.
   - Do not reuse the same copy for both platforms.

3. **Preview for approval**
   Show all of this before scheduling:
   - X copy plus character count.
   - LinkedIn copy.
   - Inferred link, if any.
   - Target accounts/integrations if already known.
   - Proposed schedule: same date, separate random times per platform.

   Ask for explicit approval. Do not schedule on "looks okay" unless it clearly approves both copy and timing.

4. **Schedule after approval**
   - Check `postiz auth:status`.
   - Run `postiz integrations:list` and select enabled `x` and `linkedin` integrations.
   - Use the user's requested date, resolving relative dates in the user's timezone.
   - Pick separate reasonable daytime random times unless the user gives exact times.
   - For X, pass `--settings '{"who_can_reply_post":"everyone"}'`; Postiz rejects X posts without it.
   - Create one post per platform.

5. **Verify**
   - Run `postiz posts:list` for the scheduled date range.
   - Confirm both returned IDs are present and queued.
   - Report local times, UTC times, post IDs, and any platform that was not scheduled.

## Approval Contract

Never call `postiz posts:create` until the user has approved:

- final X copy
- final LinkedIn copy
- schedule date
- separate random times or the rule used to choose them
- target integrations/accounts

If the user asks to "schedule it" before seeing drafts, draft first and ask approval.

## Common Failures

| Failure | Response |
|---|---|
| X copy exceeds 280 characters | Rewrite shorter before previewing. |
| Missing X reply setting | Retry only with `who_can_reply_post: everyone` after reading the error. |
| Missing or disabled integration | Stop and tell the user which platform cannot be scheduled. |
| User changes copy after approval | Preview the changed copy and ask approval again. |
| Postiz API returns a new validation error | Read the error, fix the specific missing setting, then retry once. |
