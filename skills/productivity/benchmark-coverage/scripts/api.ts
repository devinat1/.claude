import { createServer } from "node:http";
import { pathToFileURL } from "node:url";

const CATALOG_VERSION = "2026-07-30";
const CACHE_MAX_AGE_SECONDS = 300;
const DEFAULT_PORT = 8787;
const MAX_PORT = 65_535;

const anthropicClaude4 = {
  kind: "lab-report",
  publisher: "Anthropic",
  title: "Introducing Claude 4",
  url: "https://www.anthropic.com/news/claude-4",
  publishedAt: "2025-05-22",
};

const openaiGpt5 = {
  kind: "lab-report",
  publisher: "OpenAI",
  title: "Introducing GPT-5 for developers",
  url: "https://openai.com/index/introducing-gpt-5-for-developers/",
  publishedAt: "2025-08-07",
};

const anthropicSonnet46 = {
  kind: "lab-report",
  publisher: "Anthropic",
  title: "Introducing Claude Sonnet 4.6",
  url: "https://www.anthropic.com/news/claude-sonnet-4-6",
  publishedAt: "2026-02-17",
};

const passRule = {
  operator: "gte",
  threshold: 50,
  provenance: "catalog-policy",
  rationale:
    "For percentage accuracy and pass-rate metrics, at least half of benchmark items must pass.",
};

const scoring = ({
  metric,
  caveats,
}: {
  metric: string;
  caveats: string[];
}) => ({
  metric,
  unit: "percent",
  direction: "higher-is-better",
  range: { min: 0, max: 100 },
  passRule,
  caveats,
});

// ponytail: static catalog is intentional; move records to durable storage when
// independent updates or more than a few hundred benchmarks make code releases impractical.
export const benchmarks = [
  {
    id: "swe-bench-verified",
    name: "SWE-bench Verified",
    aliases: ["SWE-bench", "SWEbench Verified"],
    summary:
      "Human-validated repository issues where an agent must generate a patch that passes tests.",
    capabilities: ["software engineering", "bug fixing", "repository reasoning", "code editing"],
    domains: ["software development", "Python"],
    taskForm: "Given a repository and issue description, produce a tested code patch.",
    inputModalities: ["text", "code repository"],
    outputFormat: "repository patch",
    representativeTasks: [
      "Fix a real GitHub issue in an existing repository.",
      "Trace a bug across a codebase and submit a patch.",
    ],
    scoring: scoring({
      metric: "resolved issue pass rate",
      caveats: [
        "Results depend on scaffold, tools, subset, sampling, and test-time compute.",
        "OpenAI reported GPT-5 on a 477-task subset; Anthropic reported Claude 4 on 500 tasks.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "OpenAI and SWE-bench",
        title: "Introducing SWE-bench Verified",
        url: "https://openai.com/index/introducing-swe-bench-verified/",
        publishedAt: "2024-08-13",
      },
      anthropicClaude4,
      openaiGpt5,
    ],
    modelResults: [
      {
        modelId: "gpt-5",
        modelName: "GPT-5",
        score: 74.9,
        metric: "pass@1",
        setting: "High reasoning; 477-task subset",
        source: openaiGpt5,
      },
      {
        modelId: "claude-opus-4",
        modelName: "Claude Opus 4",
        score: 72.5,
        metric: "pass@1",
        setting: "No extended thinking; bash and editor tools; full 500 tasks",
        source: anthropicClaude4,
      },
      {
        modelId: "claude-sonnet-4",
        modelName: "Claude Sonnet 4",
        score: 72.7,
        metric: "pass@1",
        setting: "No extended thinking; bash and editor tools; full 500 tasks",
        source: anthropicClaude4,
      },
    ],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "aider-polyglot",
    name: "Aider Polyglot",
    aliases: ["Aider polyglot benchmark"],
    summary:
      "Code-editing exercises across programming languages where the answer must be emitted as a diff.",
    capabilities: ["code generation", "code editing", "instruction following"],
    domains: ["software development", "multiple programming languages"],
    taskForm: "Solve an Exercism coding exercise by producing a code diff.",
    inputModalities: ["text", "code"],
    outputFormat: "code diff",
    representativeTasks: [
      "Implement a small programming exercise in an existing file.",
      "Edit code under a precise natural-language requirement.",
    ],
    scoring: scoring({
      metric: "exercise pass rate",
      caveats: ["Prompting, edit format, and reasoning effort affect comparability."],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "Aider",
        title: "Aider LLM leaderboards",
        url: "https://aider.chat/docs/leaderboards/",
      },
      openaiGpt5,
    ],
    modelResults: [
      {
        modelId: "gpt-5",
        modelName: "GPT-5",
        score: 88,
        metric: "pass rate",
        setting: "Diff format; high reasoning",
        source: openaiGpt5,
      },
    ],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "terminal-bench",
    name: "Terminal-Bench",
    aliases: ["Terminal-Bench 1.0", "Terminal Bench"],
    summary:
      "Agentic tasks completed in isolated command-line environments and graded by tests.",
    capabilities: ["terminal use", "agentic coding", "system administration", "tool use"],
    domains: ["software development", "command line", "DevOps"],
    taskForm: "Use a terminal over multiple steps to complete a realistic task in an environment.",
    inputModalities: ["text", "terminal environment"],
    outputFormat: "modified environment",
    representativeTasks: [
      "Configure or debug software through shell commands.",
      "Build an artifact in a containerized terminal.",
    ],
    scoring: scoring({
      metric: "task pass rate",
      caveats: [
        "Agent harness, step budget, environment version, and compute materially affect scores.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "Laude Institute",
        title: "Terminal-Bench",
        url: "https://www.tbench.ai/",
      },
      anthropicClaude4,
    ],
    modelResults: [
      {
        modelId: "claude-opus-4",
        modelName: "Claude Opus 4",
        score: 43.2,
        metric: "pass@1",
        setting: "Claude Code agent; no extended thinking",
        source: anthropicClaude4,
      },
      {
        modelId: "claude-sonnet-4",
        modelName: "Claude Sonnet 4",
        score: 35.5,
        metric: "pass@1",
        setting: "Claude Code agent; no extended thinking",
        source: anthropicClaude4,
      },
    ],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "gpqa-diamond",
    name: "GPQA Diamond",
    aliases: ["GPQA-D", "Graduate-Level Google-Proof Q&A Diamond"],
    summary:
      "Expert-written, graduate-level multiple-choice questions in biology, physics, and chemistry.",
    capabilities: ["scientific reasoning", "expert knowledge", "question answering"],
    domains: ["biology", "physics", "chemistry"],
    taskForm: "Answer a difficult graduate-level multiple-choice science question.",
    inputModalities: ["text"],
    outputFormat: "multiple-choice answer",
    representativeTasks: [
      "Solve a PhD-level physics question.",
      "Reason through an expert chemistry or biology question.",
    ],
    scoring: scoring({
      metric: "accuracy",
      caveats: [
        "Closed-book, tool use, prompting, and extended thinking settings are not interchangeable.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "David Rein et al.",
        title: "GPQA: A Graduate-Level Google-Proof Q&A Benchmark",
        url: "https://github.com/idavidrein/gpqa",
        publishedAt: "2023-11-20",
      },
      anthropicClaude4,
    ],
    modelResults: [
      {
        modelId: "claude-opus-4",
        modelName: "Claude Opus 4",
        score: 79.6,
        metric: "accuracy",
        setting: "Extended thinking, up to 64K tokens",
        source: anthropicClaude4,
      },
      {
        modelId: "claude-sonnet-4",
        modelName: "Claude Sonnet 4",
        score: 75.4,
        metric: "accuracy",
        setting: "Extended thinking, up to 64K tokens",
        source: anthropicClaude4,
      },
    ],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "tau2-bench",
    name: "τ²-bench",
    aliases: ["tau2-bench", "tau-bench"],
    summary:
      "Tool-agent-user interactions where both the agent and simulated user can change shared state.",
    capabilities: ["tool use", "policy following", "multi-turn interaction", "state tracking"],
    domains: ["customer service", "telecom", "airline", "retail"],
    taskForm:
      "Complete a multi-turn service task by following policy and calling tools while state changes.",
    inputModalities: ["text", "tool results"],
    outputFormat: "tool calls and conversational response",
    representativeTasks: [
      "Resolve a customer-service request under a policy.",
      "Coordinate tool calls while the user changes task state.",
    ],
    scoring: scoring({
      metric: "task success rate",
      caveats: [
        "Domain, simulator, policy version, and tool harness must match for score comparison.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "Sierra Research",
        title: "τ²-bench",
        url: "https://github.com/sierra-research/tau2-bench",
      },
      openaiGpt5,
    ],
    modelResults: [
      {
        modelId: "gpt-5",
        modelName: "GPT-5",
        score: 96.7,
        metric: "success rate",
        setting: "Telecom domain; reported at launch",
        source: openaiGpt5,
      },
    ],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "mmmu",
    name: "MMMU",
    aliases: ["Massive Multi-discipline Multimodal Understanding"],
    summary:
      "College-level multimodal questions requiring image understanding, domain knowledge, and reasoning.",
    capabilities: ["multimodal reasoning", "visual understanding", "expert knowledge"],
    domains: ["art", "business", "science", "health", "humanities", "engineering"],
    taskForm: "Answer a college-level question using both visual and textual evidence.",
    inputModalities: ["text", "image"],
    outputFormat: "multiple-choice or short answer",
    representativeTasks: [
      "Interpret a technical diagram to answer a domain question.",
      "Reason over a chart, map, table, or scientific image.",
    ],
    scoring: scoring({
      metric: "validation accuracy",
      caveats: ["MMMU and MMMU-Pro are distinct variants and must not share results."],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "MMMU Benchmark",
        title: "MMMU",
        url: "https://github.com/MMMU-Benchmark/MMMU",
        publishedAt: "2023-11-27",
      },
      anthropicClaude4,
    ],
    modelResults: [
      {
        modelId: "claude-opus-4",
        modelName: "Claude Opus 4",
        score: 76.5,
        metric: "validation accuracy",
        setting: "Extended thinking, up to 64K tokens",
        source: anthropicClaude4,
      },
      {
        modelId: "claude-sonnet-4",
        modelName: "Claude Sonnet 4",
        score: 74.4,
        metric: "validation accuracy",
        setting: "Extended thinking, up to 64K tokens",
        source: anthropicClaude4,
      },
    ],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "aime-2025",
    name: "AIME 2025",
    aliases: ["American Invitational Mathematics Examination 2025"],
    summary:
      "Competition mathematics problems used by frontier labs to evaluate multi-step mathematical reasoning.",
    capabilities: ["mathematical reasoning", "problem solving"],
    domains: ["mathematics"],
    taskForm: "Solve a competition mathematics problem and return an exact integer answer.",
    inputModalities: ["text"],
    outputFormat: "integer answer",
    representativeTasks: [
      "Solve a multi-step olympiad-style algebra problem.",
      "Produce an exact answer to a difficult geometry or number-theory problem.",
    ],
    scoring: scoring({
      metric: "accuracy",
      caveats: [
        "AIME is an exam reused as an evaluation; sampling and answer-extraction methods matter.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "Mathematical Association of America",
        title: "American Invitational Mathematics Examination",
        url: "https://maa.org/math-competitions/american-invitational-mathematics-examination-aime/",
      },
      anthropicClaude4,
    ],
    modelResults: [
      {
        modelId: "claude-opus-4",
        modelName: "Claude Opus 4",
        score: 75.5,
        metric: "accuracy",
        setting: "Extended thinking with parallel test-time compute",
        source: anthropicClaude4,
      },
      {
        modelId: "claude-sonnet-4",
        modelName: "Claude Sonnet 4",
        score: 70.5,
        metric: "accuracy",
        setting: "Extended thinking with parallel test-time compute",
        source: anthropicClaude4,
      },
    ],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "humanitys-last-exam",
    name: "Humanity's Last Exam",
    aliases: ["HLE"],
    summary:
      "Broad expert-level closed-ended questions across more than one hundred academic subjects.",
    capabilities: ["expert knowledge", "scientific reasoning", "question answering"],
    domains: ["mathematics", "science", "humanities", "engineering", "social science"],
    taskForm: "Answer a difficult expert-authored multiple-choice or short-answer question.",
    inputModalities: ["text", "image"],
    outputFormat: "multiple-choice or short answer",
    representativeTasks: [
      "Answer a precise expert-level question that resists simple retrieval.",
      "Solve a closed-ended question requiring specialist knowledge.",
    ],
    scoring: scoring({
      metric: "accuracy",
      caveats: [
        "Tool-enabled and no-tool results are separate settings.",
        "High aggregate accuracy does not establish general intelligence or autonomous research ability.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "Center for AI Safety and Scale AI",
        title: "Humanity's Last Exam",
        url: "https://www.lastexam.ai/",
        publishedAt: "2025-01-23",
      },
      anthropicSonnet46,
    ],
    modelResults: [],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "browsecomp",
    name: "BrowseComp",
    aliases: ["Browsing Competition"],
    summary:
      "Hard, multi-hop web research questions with short, verifiable answers.",
    capabilities: ["web research", "information retrieval", "multi-hop reasoning", "tool use"],
    domains: ["open domain"],
    taskForm: "Search the web persistently to identify one obscure fact from multiple clues.",
    inputModalities: ["text", "web pages"],
    outputFormat: "short answer",
    representativeTasks: [
      "Identify an obscure entity by connecting clues across many sources.",
      "Find a hard-to-locate fact and return a verifiable short answer.",
    ],
    scoring: scoring({
      metric: "accuracy",
      caveats: [
        "Browsing tools, search index, time budget, and sampling strategy materially affect results.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "OpenAI",
        title: "BrowseComp: a benchmark for browsing agents",
        url: "https://openai.com/index/browsecomp/",
        publishedAt: "2025-04-10",
      },
      anthropicSonnet46,
    ],
    modelResults: [],
    updatedAt: CATALOG_VERSION,
  },
  {
    id: "osworld-verified",
    name: "OSWorld-Verified",
    aliases: ["OSWorld"],
    summary:
      "Open-ended computer tasks performed in real web and desktop applications.",
    capabilities: ["computer use", "visual grounding", "tool use", "long-horizon planning"],
    domains: ["desktop applications", "web applications", "operating systems"],
    taskForm: "Operate a computer through visual interaction to complete a multi-step workflow.",
    inputModalities: ["text", "screenshot", "computer state"],
    outputFormat: "modified application state",
    representativeTasks: [
      "Edit a document through a desktop application.",
      "Complete a workflow spanning browser and operating-system applications.",
    ],
    scoring: scoring({
      metric: "task success rate",
      caveats: [
        "OSWorld and OSWorld-Verified use different task quality and grading infrastructure.",
        "Computer-use harness, step budget, and environment version affect results.",
      ],
    }),
    sources: [
      {
        kind: "benchmark",
        publisher: "XLang Lab",
        title: "OSWorld",
        url: "https://osworld-v1.xlang.ai/",
        publishedAt: "2024-04-11",
      },
      anthropicSonnet46,
    ],
    modelResults: [],
    updatedAt: CATALOG_VERSION,
  },
];

const catalogRules = {
  data: [
    "Include a benchmark only with a primary benchmark source and evidence that a leading lab uses it.",
    "Store model results only when an identified source reports the exact model, score, metric, and setting.",
    "Never infer missing model results or merge scores across benchmark variants.",
  ],
  retrieval: [
    "The API performs lexical candidate retrieval, not semantic coverage matching.",
    "q matches words across names, aliases, summaries, capabilities, domains, task forms, and representative tasks.",
    "capability and domain filters are case-insensitive exact filters.",
    "model trims modelResults but never removes an otherwise matching benchmark.",
  ],
  coverage: [
    "The consuming agent must require overlap in core capability and task form.",
    "Domain overlap is supporting evidence, not a requirement.",
    "Weak matches must be rejected rather than forced.",
  ],
  performance: [
    "Apply each benchmark's passRule only to an exact model result returned by the API.",
    "A missing exact model result means insufficient evidence.",
    "Aggregate benchmark scores are proxies and do not guarantee one prompt will pass.",
  ],
};

const benchmarkRecordSchema = {
  $schema: "https://json-schema.org/draft/2020-12/schema",
  $id: "https://benchmark-coverage.local/schemas/benchmark-record.v1.json",
  title: "BenchmarkRecord",
  type: "object",
  additionalProperties: false,
  required: [
    "id",
    "name",
    "aliases",
    "summary",
    "capabilities",
    "domains",
    "taskForm",
    "inputModalities",
    "outputFormat",
    "representativeTasks",
    "scoring",
    "sources",
    "modelResults",
    "updatedAt",
  ],
  properties: {
    id: { type: "string", pattern: "^[a-z0-9-]+$" },
    name: { type: "string", minLength: 1 },
    aliases: { type: "array", items: { type: "string" } },
    summary: { type: "string", minLength: 1 },
    capabilities: { type: "array", minItems: 1, items: { type: "string" } },
    domains: { type: "array", minItems: 1, items: { type: "string" } },
    taskForm: { type: "string", minLength: 1 },
    inputModalities: { type: "array", minItems: 1, items: { type: "string" } },
    outputFormat: { type: "string", minLength: 1 },
    representativeTasks: { type: "array", minItems: 1, items: { type: "string" } },
    scoring: {
      type: "object",
      additionalProperties: false,
      required: ["metric", "unit", "direction", "range", "passRule", "caveats"],
      properties: {
        metric: { type: "string" },
        unit: { const: "percent" },
        direction: { const: "higher-is-better" },
        range: {
          type: "object",
          additionalProperties: false,
          required: ["min", "max"],
          properties: { min: { const: 0 }, max: { const: 100 } },
        },
        passRule: {
          type: "object",
          additionalProperties: false,
          required: ["operator", "threshold", "provenance", "rationale"],
          properties: {
            operator: { const: "gte" },
            threshold: { type: "number", minimum: 0, maximum: 100 },
            provenance: { enum: ["official", "catalog-policy"] },
            rationale: { type: "string" },
          },
        },
        caveats: { type: "array", items: { type: "string" } },
      },
    },
    sources: {
      type: "array",
      minItems: 2,
      items: { $ref: "#/$defs/source" },
    },
    modelResults: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["modelId", "modelName", "score", "metric", "setting", "source"],
        properties: {
          modelId: { type: "string" },
          modelName: { type: "string" },
          score: { type: "number", minimum: 0, maximum: 100 },
          metric: { type: "string" },
          setting: { type: "string" },
          source: { $ref: "#/$defs/source" },
        },
      },
    },
    updatedAt: { type: "string", format: "date" },
  },
  $defs: {
    source: {
      type: "object",
      additionalProperties: false,
      required: ["kind", "publisher", "title", "url"],
      properties: {
        kind: { enum: ["benchmark", "lab-report"] },
        publisher: { type: "string" },
        title: { type: "string" },
        url: { type: "string", format: "uri" },
        publishedAt: { type: "string", format: "date" },
      },
    },
  },
};

const responseSchemas = {
  BenchmarkRecord: benchmarkRecordSchema,
  BenchmarkListResponse: {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    title: "BenchmarkListResponse",
    type: "object",
    additionalProperties: false,
    required: ["apiVersion", "catalogVersion", "data", "query"],
    properties: {
      apiVersion: { const: "v1" },
      catalogVersion: { type: "string" },
      data: { type: "array", items: benchmarkRecordSchema },
      query: {
        type: "object",
        additionalProperties: false,
        properties: {
          q: { type: "string" },
          capability: { type: "string" },
          domain: { type: "string" },
          model: { type: "string" },
        },
      },
    },
  },
  ErrorResponse: {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    title: "ErrorResponse",
    type: "object",
    additionalProperties: false,
    required: ["error"],
    properties: {
      error: {
        type: "object",
        additionalProperties: false,
        required: ["code", "message"],
        properties: {
          code: { type: "string" },
          message: { type: "string" },
        },
      },
    },
  },
};

const normalize = ({ value }: { value: string }) =>
  value
    .normalize("NFKD")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .trim();

const createJsonResponse = ({
  value,
  status,
}: {
  value: unknown;
  status?: number | null;
}) => {
  const responseStatus = status ?? 200;
  return Response.json(value, {
    status: responseStatus,
    headers: {
      "cache-control":
        responseStatus === 200
          ? `public, max-age=${CACHE_MAX_AGE_SECONDS}`
          : "no-store",
      "content-type": "application/json; charset=utf-8",
    },
  });
};

const createErrorResponse = ({
  status,
  code,
  message,
}: {
  status: number;
  code: string;
  message: string;
}) => createJsonResponse({ value: { error: { code, message } }, status });

function searchBenchmarks({ url }: { url: URL }) {
  const searchQuery = url.searchParams.get("q")?.trim() || undefined;
  const capability = url.searchParams.get("capability")?.trim() || undefined;
  const domain = url.searchParams.get("domain")?.trim() || undefined;
  const model = url.searchParams.get("model")?.trim() || undefined;

  const searchTerms = normalize({ value: searchQuery ?? "" })
    .split(" ")
    .filter((searchTerm) => searchTerm.length > 0);
  const normalizedCapability = normalize({ value: capability ?? "" });
  const normalizedDomain = normalize({ value: domain ?? "" });
  const normalizedModel = normalize({ value: model ?? "" });

  const matchingBenchmarks = benchmarks
    .map((record) => {
      const searchableRecord = normalize({
        value: [
          record.name,
          ...record.aliases,
          record.summary,
          ...record.capabilities,
          ...record.domains,
          record.taskForm,
          ...record.representativeTasks,
        ].join(" "),
      });
      const rank = searchTerms.reduce(
        (total, searchTerm) => total + (searchableRecord.includes(searchTerm) ? 1 : 0),
        0,
      );
      return { record, rank };
    })
    .filter(({ record, rank }) => {
      if (searchTerms.length > 0 && rank === 0) return false;
      if (
        normalizedCapability.length > 0 &&
        !record.capabilities.some(
          (recordCapability) =>
            normalize({ value: recordCapability }) === normalizedCapability,
        )
      ) {
        return false;
      }
      if (
        normalizedDomain.length > 0 &&
        !record.domains.some(
          (recordDomain) => normalize({ value: recordDomain }) === normalizedDomain,
        )
      ) {
        return false;
      }
      return true;
    })
    .toSorted(
      (firstMatch, secondMatch) =>
        secondMatch.rank - firstMatch.rank ||
        firstMatch.record.id.localeCompare(secondMatch.record.id),
    )
    .map(({ record }) => ({
      ...record,
      modelResults:
        normalizedModel.length > 0
          ? record.modelResults.filter(
              (modelResult) =>
                normalize({ value: modelResult.modelId }) === normalizedModel,
            )
          : record.modelResults,
    }));

  return {
    apiVersion: "v1",
    catalogVersion: CATALOG_VERSION,
    data: matchingBenchmarks,
    query: { q: searchQuery, capability, domain, model },
  };
}

export function handleRequest({ request }: { request: Request }): Response {
  if (request.method !== "GET") {
    return createErrorResponse({
      status: 405,
      code: "method_not_allowed",
      message: "Only GET is supported.",
    });
  }

  const url = new URL(request.url);
  if (url.pathname === "/v1/schema") {
    return createJsonResponse({ value: { apiVersion: "v1", schemas: responseSchemas } });
  }
  if (url.pathname === "/v1/rules") {
    return createJsonResponse({ value: catalogRules });
  }
  if (url.pathname === "/v1/benchmarks") {
    return createJsonResponse({ value: searchBenchmarks({ url }) });
  }

  return createErrorResponse({
    status: 404,
    code: "not_found",
    message: "Route not found.",
  });
}

function startServer() {
  const port = Number(process.env.PORT ?? DEFAULT_PORT);
  if (!Number.isInteger(port) || port < 1 || port > MAX_PORT) {
    throw new Error(`PORT must be an integer from 1 to ${MAX_PORT}.`);
  }

  createServer(async (request, response) => {
    const result = handleRequest({
      request: new Request(
        new URL(request.url ?? "/", `http://127.0.0.1:${port}`),
        { method: request.method },
      ),
    });
    response.writeHead(result.status, Object.fromEntries(result.headers));
    response.end(Buffer.from(await result.arrayBuffer()));
  }).listen(port, "127.0.0.1", () => {
    console.log(`Benchmark catalog listening on http://127.0.0.1:${port}.`);
  });
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  startServer();
}
