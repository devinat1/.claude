---
name: webmcp-bridge
description: Use when working with the generic WebMCP Chrome bridge extension, its generated-tool cache, or external browser harnesses like Playwright, Codex, Claude Code, or CodeHawke that should generate, import, and execute page-specific tools instead of implementing a chat UI.
---

# WebMCP Bridge

Use this skill when the user wants an external agent or browser harness to work through the WebMCP Chrome extension. The supported product is a generic all-pages bridge and generated-tool runtime: the extension exposes page diagnostics, sanitized page evidence, a tool cache, and a stable execution surface; the harness owns reasoning, generation, navigation, approvals, and verification.

## Core Rule

Do not design or add an extension-owned chat UI, OpenAI API key storage, LLM calls, generic browser automation tools, or extension-owned benchmark automation unless the user explicitly asks for that. The extension is the runtime and cache; Codex, Claude Code, Playwright, CodeHawke, or another harness generates tool JSON outside the extension and imports it back.

## Supported Surface

The extension requests broad `<all_urls>` host access and injects on every Chrome-allowed page when all-sites access is enabled. It exposes:

- `window.__WEBMCP_BRIDGE__` for `getDiagnostics()`, `listTools()`, and `executeTool({ name, input })`.
- `window.__WEBMCP_TOOL_CACHE__` for `getSanitizedTrace()`, `importGeneratedTools({ tools })`, and generated-tool listing.

Generic pages start with zero tools. A `WebMCP tools loaded: 0` toast is expected unless a static adapter matches or generated tools were previously imported and rehydrated from `chrome.storage.local`. `window.__WEBMCP_SUPPORTED_SITE_TOOLS__` is only a legacy alias.

AWS IAM is currently the only built-in static adapter. It contributes `aws_iam_get_access_key_state`, `aws_iam_create_access_key`, and `aws_iam_deactivate_access_key` only on AWS Console pages.

## Bridge Check

When connected to a page, first wait for the active extension surface from the browser context:

```js
await page.waitForFunction(() =>
  Boolean(window.__WEBMCP_BRIDGE__ && window.__WEBMCP_TOOL_CACHE__)
);
```

If the page was already open before loading the unpacked extension, reload it once. If the bridge is still missing, use the extension action as a retry or post `WEBMCP_EXTENSION_ENABLE` from the harness. The extension panel is for status and diagnostics, not chat.

## Diagnostics

Use bridge diagnostics before attempting execution:

```js
const diagnostics = await page.evaluate(() =>
  window.__WEBMCP_BRIDGE__.getDiagnostics()
);
```

Confirm `supportedSite.siteId`, tool count, tool names, input schemas, and risk annotations. On generic pages, `supportedSite.siteId` is the current page origin. Empty `tools` means the bridge loaded but no tool is available yet.

## Generated Tool Flow

When no listed tool matches the user goal, the harness can generate one from sanitized evidence:

```js
const trace = await page.evaluate(() =>
  window.__WEBMCP_TOOL_CACHE__.getSanitizedTrace()
);
```

Generate the WebMCP tool JSON outside the extension from the trace and the user goal. Do not include cookies, auth headers, tokens, passwords, credentials, API keys, session values, or secret-shaped strings.

Import generated tools back into the page runtime:

```js
await page.evaluate(
  ({ tools }) => window.__WEBMCP_TOOL_CACHE__.importGeneratedTools({ tools }),
  { tools: generatedTools },
);
```

Then verify the import through the bridge:

```js
await page.evaluate(() => window.__WEBMCP_BRIDGE__.listTools());
```

Imported generated tools are append-only and persisted in `chrome.storage.local`, so page reloads can hydrate them without rebuilding the extension.

## Tool Execution

Execute static or generated tools through the same bridge:

```js
await page.evaluate(
  ({ name, input }) => window.__WEBMCP_BRIDGE__.executeTool({ name, input }),
  { name: "tool_name", input: {} },
);
```

Use tool input schemas and risk annotations from diagnostics to build arguments and decide whether approval is needed. After execution, verify the page state directly with the harness.

## Harness Boundary

Use Playwright or the active browser harness for generic browser work: navigation, clicking, filling fields, scrolling, screenshots, waiting, visual inspection, and fallback recovery. Use the bridge for static adapter tools and generated semantic tools that have been imported into the extension runtime.

If no listed tool fits and generating a tool is not warranted, continue with normal harness automation rather than adding broad automation primitives to the extension.

## Implementation Guidance

If asked to modify the extension, keep it bridge-only by default:

- Preserve `navigator.modelContext.registerTool(...)` and `document.modelContext` compatibility.
- Do not override a native WebMCP provider; report native-provider state instead.
- Expose a stable `window.__WEBMCP_BRIDGE__` with `getDiagnostics()`, `listTools()`, and `executeTool({ name, input })`.
- Expose `window.__WEBMCP_TOOL_CACHE__` with sanitized trace capture and generated-tool import.
- Dispatch a page event such as `webmcp:ready` after bridge installation so late-connected pages can register tools.
- Keep generic pages functional with an empty initial registry.
- Keep the UI limited to connection status, page diagnostics, and registered tools.

## Failure Handling

Treat tool failures as tool-contract failures first. Inspect diagnostics, page console output, and the current page state before changing extension code. For AWS create/deactivate tools, require a disposable account or explicit user approval because they can change credentials and return a newly created secret access key once.
