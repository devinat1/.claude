---
name: webmcp-bridge
description: Use when an external Playwright, Codex, Claude Code, or browser harness must generate, import, and invoke page-specific tools through the generic WebMCP Chrome extension.
---

# WebMCP Bridge

The extension is only a page runtime and generated-tool cache. The active harness owns Chrome setup, navigation, reasoning, approvals, credentials, invocation, and verification.

## Start Chrome Beta

From the WebMCP repository, install dependencies once when `extension/node_modules` is missing, then open the profile:

```bash
test -d extension/node_modules || make install
make chrome-beta-profile-open CHROME_BETA_START_URL=chrome://extensions/
```

The helper reuses the existing Chrome Beta debugging endpoint and opens the dedicated profile only when that endpoint is unavailable. If the extension is not loaded, tell the user to enable Developer mode and load `extension/` unpacked, then wait. Never install it for them. Reload the target page after loading.

The caller supplies Playwright; this repository has no browser-client dependency or model key.

## Per-page loop

Repeat after every navigation:

1. Wait for both `window.__WEBMCP_BRIDGE__` and `window.__WEBMCP_TOOL_CACHE__`. A generic page correctly starts with zero tools.
2. Read `getDiagnostics()`, `listTools()`, and `getSanitizedTrace()`.
3. Give the agent only `trace.page` and `trace.dom.interactiveElements`. Do not expose HTML, network history, cookies, auth headers, tokens, passwords, or other secret values.
4. Choose one visible semantic action. Build one generated tool with one `dom.click`, `dom.fill`, or `dom.select` step. Its selector must occur in the trace; its origin, path, and URL must exactly match the current page; its object schema must reject extra properties; its name must be unique.
5. Import it with `__WEBMCP_TOOL_CACHE__.importGeneratedTools({ tools: [tool] })`, require `ok: true`, then confirm it through `__WEBMCP_BRIDGE__.listTools()`.
6. Invoke only through native CDP. After completion, verify the live page and repeat. Once a semantic action is chosen, never substitute a direct Playwright click or fill.

```js
const cdpSession = await page.context().newCDPSession(page);
const { frameTree } = await cdpSession.send("Page.getFrameTree");
await cdpSession.send("WebMCP.enable");
const responsePromise = new Promise((resolve) => {
  cdpSession.once("WebMCP.toolResponded", resolve);
});
const invocation = await cdpSession.send("WebMCP.invokeTool", {
  frameId: frameTree.frame.id,
  toolName: generatedTool.name,
  input: generatedInput,
});
const response = await responsePromise;
if (response.invocationId !== invocation.invocationId || response.status !== "Completed") {
  throw new Error(response.errorText ?? "Native WebMCP invocation failed.");
}
```

## Failure handling

Treat missing globals, unavailable native `document.modelContext.registerTool`, rejected scope/schema/selector, duplicate names, failed import, mismatched invocation ids, non-completed responses, and failed page verification as hard stops. Re-read the page after navigation or stale selectors, generate a fresh tool, and retry through WebMCP. Do not add site adapters, broad automation tools, an extension chat UI, LLM calls, or credential storage.
