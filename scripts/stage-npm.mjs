#!/usr/bin/env node
// Stage the Python package's module resources at the npm package root.
import { cpSync, existsSync, readdirSync, rmSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const inner = "spec_clauses_us_health";
if (!statSync(join(root, inner)).isDirectory()) {
  console.error(`stage-npm: module directory ${inner} is missing`);
  process.exit(1);
}

const payload = ["manifest.yaml", "clauses"];
for (const item of payload) {
  const target = join(root, item);
  if (process.argv.includes("--clean")) {
    rmSync(target, { recursive: true, force: true });
    continue;
  }
  const source = join(root, inner, item);
  if (existsSync(target)) rmSync(target, { recursive: true, force: true });
  if (existsSync(source)) cpSync(source, target, { recursive: true });
}
