import assert from "node:assert/strict";
import test from "node:test";

import { benchmarks, handleRequest } from "./api.ts";

const getApiResponse = async ({ path }: { path: string }) => {
  const response = handleRequest({
    request: new Request(`http://catalog.test${path}`),
  });
  return { response, responseBody: await response.json() };
};

test("returns source-backed coding matches and trims model results", async () => {
  const { response, responseBody } = await getApiResponse({
    path: "/v1/benchmarks?q=repository%20patch&model=gpt-5",
  });

  assert.equal(response.status, 200);
  assert.equal(responseBody.data[0].id, "swe-bench-verified");
  assert.deepEqual(responseBody.query, {
    q: "repository patch",
    model: "gpt-5",
  });
  assert.deepEqual(
    responseBody.data[0].modelResults.map(({ modelId }: { modelId: string }) => modelId),
    ["gpt-5"],
  );
  assert.ok(
    responseBody.data[0].sources.some(
      ({ kind }: { kind: string }) => kind === "benchmark",
    ),
  );
  assert.ok(
    responseBody.data[0].sources.some(
      ({ kind }: { kind: string }) => kind === "lab-report",
    ),
  );
});

test("catalog records keep source and score invariants", () => {
  assert.equal(new Set(benchmarks.map(({ id }) => id)).size, benchmarks.length);
  assert.ok(
    benchmarks.every((record) =>
      record.sources.some(({ kind }) => kind === "benchmark"),
    ),
  );
  assert.ok(
    benchmarks.every((record) =>
      record.sources.some(({ kind }) => kind === "lab-report"),
    ),
  );
  assert.ok(
    benchmarks.every((record) =>
      record.modelResults.every(
        (modelResult) => modelResult.score >= 0 && modelResult.score <= 100,
      ),
    ),
  );
  assert.ok(
    benchmarks.every((record) =>
      record.modelResults.every((modelResult) =>
        record.sources.some(({ url }) => url === modelResult.source.url),
      ),
    ),
  );
});

test("filters records and rejects unsupported requests", async () => {
  const filteredResponse = await getApiResponse({
    path: "/v1/benchmarks?capability=multimodal%20reasoning&domain=engineering",
  });
  assert.deepEqual(
    filteredResponse.responseBody.data.map(({ id }: { id: string }) => id),
    ["mmmu"],
  );

  const unsupportedMethodResponse = handleRequest({
    request: new Request("http://catalog.test/v1/benchmarks", { method: "POST" }),
  });
  assert.equal(unsupportedMethodResponse.status, 405);

  const unknownRouteResponse = await getApiResponse({ path: "/unknown" });
  assert.equal(unknownRouteResponse.response.status, 404);
});

test("publishes matching response schemas and rules", async () => {
  const schema = await getApiResponse({ path: "/v1/schema" });
  assert.equal(schema.responseBody.schemas.BenchmarkRecord.title, "BenchmarkRecord");
  assert.equal(
    schema.responseBody.schemas.BenchmarkListResponse.title,
    "BenchmarkListResponse",
  );
  assert.equal(schema.responseBody.schemas.ErrorResponse.title, "ErrorResponse");
  assert.deepEqual(
    schema.responseBody.schemas.BenchmarkRecord.required.toSorted(),
    Object.keys(benchmarks[0]).toSorted(),
  );

  const rules = await getApiResponse({ path: "/v1/rules" });
  assert.ok(
    rules.responseBody.performance.includes(
      "A missing exact model result means insufficient evidence.",
    ),
  );
});
