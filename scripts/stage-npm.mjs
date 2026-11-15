#!/usr/bin/env node
// Stage the Python package's module resources at the npm package root.
import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const inner = "spec_clauses_us_health";
const payload = ["manifest.yaml", "clauses"];

function restoreOriginals() {
  const backupRoot = join(root, ".npm-stage-backup");
  const marker = join(backupRoot, "owned.json");
  if (!existsSync(marker)) return;
  const { originals } = JSON.parse(readFileSync(marker, "utf8"));

  for (const item of payload) {
    const backup = join(backupRoot, item);
    const target = join(root, item);
    if (existsSync(backup)) {
      rmSync(target, { recursive: true, force: true });
      renameSync(backup, target);
    } else if (!originals.includes(item)) {
      rmSync(target, { recursive: true, force: true });
    }
  }
  rmSync(backupRoot, { recursive: true, force: true });
}

if (process.argv.includes("--clean")) {
  restoreOriginals();
  process.exit(0);
}

const backupRoot = join(root, ".npm-stage-backup");
if (existsSync(backupRoot)) {
  console.error("stage-npm: unfinished staging backup exists; run --clean to restore it");
  process.exit(1);
}
if (!existsSync(join(root, inner)) || !statSync(join(root, inner)).isDirectory()) {
  console.error(`stage-npm: module directory ${inner} is missing`);
  process.exit(1);
}

mkdirSync(backupRoot);
const originals = payload.filter((item) => existsSync(join(root, item)));
writeFileSync(
  join(backupRoot, "owned.json"),
  JSON.stringify({ version: 1, originals }),
);
try {
  for (const item of payload) {
    const target = join(root, item);
    if (existsSync(target)) renameSync(target, join(backupRoot, item));
    const source = join(root, inner, item);
    if (existsSync(source)) cpSync(source, target, { recursive: true });
  }
} catch (error) {
  restoreOriginals();
  throw error;
}
