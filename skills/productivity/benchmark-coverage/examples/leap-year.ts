import assert from "node:assert/strict";

export function isLeapYear(year: number): boolean {
  throw new Error(`Not implemented for ${year}`);
}

assert.equal(isLeapYear(1996), true);
assert.equal(isLeapYear(1900), false);
assert.equal(isLeapYear(2000), true);
assert.equal(isLeapYear(2019), false);
