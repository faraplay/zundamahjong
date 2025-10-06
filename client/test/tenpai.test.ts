import { expect, test } from "vitest";
import { check_tenpai } from "../src/shanten";

test("Test the waits for not_tenpai", () => {
  expect(check_tenpai([1, 2, 4, 5, 6, 13, 14, 14, 15, 15, 16, 31, 32])).toEqual(
    new Set(),
  );
});

test("Test the waits for four_of_a_kind", () => {
  expect(check_tenpai([2, 2, 2, 2])).toEqual(new Set([2]));
});

test("Test the waits for ryanmen", () => {
  expect(check_tenpai([4, 5, 31, 31])).toEqual(new Set([3, 6]));
});

test("Test the waits for shanpon", () => {
  expect(check_tenpai([4, 4, 19, 19])).toEqual(new Set([4, 19]));
});

test("Test the waits for kanchan", () => {
  expect(check_tenpai([3, 5, 31, 31])).toEqual(new Set([4]));
});

test("Test the waits for penchan", () => {
  expect(check_tenpai([8, 9, 31, 31])).toEqual(new Set([7]));
});

test("Test the waits for tanki", () => {
  expect(check_tenpai([31])).toEqual(new Set([31]));
});

test("Test the waits for nakabukure", () => {
  expect(check_tenpai([3, 4, 4, 5])).toEqual(new Set([4]));
});

test("Test the waits for nobetan", () => {
  expect(check_tenpai([2, 3, 4, 5])).toEqual(new Set([2, 5]));
});

test("Test the waits for sanmenchan", () => {
  expect(check_tenpai([2, 3, 4, 5, 6, 31, 31])).toEqual(new Set([1, 4, 7]));
});

test("Test the waits for sanmentan", () => {
  expect(check_tenpai([2, 3, 4, 5, 6, 7, 8])).toEqual(new Set([2, 5, 8]));
});

test("Test the waits for sanmen_shanpon", () => {
  expect(check_tenpai([4, 4, 5, 5, 6, 6, 7, 7, 31, 31])).toEqual(
    new Set([4, 7, 31]),
  );
});

test("Test the waits for entotsu", () => {
  expect(check_tenpai([4, 5, 6, 6, 6, 31, 31])).toEqual(new Set([3, 6, 31]));
});

test("Test the waits for aryanmen", () => {
  expect(check_tenpai([6, 7, 8, 8])).toEqual(new Set([5, 8]));
});

test("Test the waits for ryantan", () => {
  expect(check_tenpai([4, 5, 5, 5])).toEqual(new Set([3, 4, 6]));
});

test("Test the waits for pentan", () => {
  expect(check_tenpai([1, 2, 2, 2])).toEqual(new Set([1, 3]));
});

test("Test the waits for kantan", () => {
  expect(check_tenpai([5, 7, 7, 7])).toEqual(new Set([5, 6]));
});

test("Test the waits for kantankan", () => {
  expect(check_tenpai([3, 3, 3, 5, 7, 7, 7])).toEqual(new Set([4, 5, 6]));
});

test("Test the waits for goren_toitsu", () => {
  expect(check_tenpai([5, 5, 6, 6, 7, 7, 8, 8, 9, 9])).toEqual(
    new Set([5, 6, 8, 9]),
  );
});

test("Test the waits for tatsumaki", () => {
  expect(check_tenpai([6, 6, 6, 7, 8, 8, 8])).toEqual(new Set([5, 6, 7, 8, 9]));
});

test("Test the waits for happoubijin", () => {
  expect(check_tenpai([2, 2, 2, 3, 4, 5, 6, 7, 7, 7])).toEqual(
    new Set([1, 2, 3, 4, 5, 6, 7, 8]),
  );
});

test("Test the waits for seven_pairs", () => {
  expect(check_tenpai([1, 1, 3, 3, 5, 5, 8, 8, 11, 11, 14, 14, 15])).toEqual(
    new Set([15]),
  );
});

test("Test the waits for thirteen_orphans", () => {
  expect(
    check_tenpai([1, 9, 9, 11, 19, 21, 31, 32, 33, 34, 35, 36, 37]),
  ).toEqual(new Set([29]));
});

test("Test the waits for thirteen_orphans_thirteen_wait", () => {
  expect(
    check_tenpai([1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]),
  ).toEqual(new Set([1, 9, 11, 19, 21, 29, 31, 32, 33, 34, 35, 36, 37]));
});
