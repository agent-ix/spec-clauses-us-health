#!/usr/bin/env node
// Stage the Python package's module resources at the npm package root.
import {
  cpSync,
  chmodSync,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  rmdirSync,
  rmSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const inner = "spec_clauses_us_health";
const payload = ["manifest.yaml", "clauses"];
const unownedBackupMessage =
  "stage-npm: .npm-stage-backup has no ownership marker and contains data; inspect and remove the unowned data before retrying";

function removeEmptyMarkerlessBackup(backupRoot) {
  if (!existsSync(backupRoot)) return true;
  try {
    rmdirSync(backupRoot);
    return true;
  } catch (error) {
    if (error.code === "ENOTEMPTY" || error.code === "EEXIST") return false;
    throw error;
  }
}

function restoreOriginals() {
  const backupRoot = join(root, ".npm-stage-backup");
  const marker = join(backupRoot, "owned.json");
  if (!existsSync(marker)) {
    return removeEmptyMarkerlessBackup(backupRoot);
  }
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
  return true;
}

if (process.argv.includes("--clean")) {
  if (!restoreOriginals()) {
    console.error(unownedBackupMessage);
    process.exit(1);
  }
  process.exit(0);
}

const backupRoot = join(root, ".npm-stage-backup");
if (existsSync(backupRoot)) {
  if (!existsSync(join(backupRoot, "owned.json"))) {
    if (!removeEmptyMarkerlessBackup(backupRoot)) {
      console.error(unownedBackupMessage);
      process.exit(1);
    }
  } else {
    console.error(
      "stage-npm: unfinished staging backup exists; run --clean to restore it",
    );
    process.exit(1);
  }
}
if (!existsSync(join(root, inner)) || !statSync(join(root, inner)).isDirectory()) {
  console.error(`stage-npm: module directory ${inner} is missing`);
  process.exit(1);
}

mkdirSync(backupRoot);
const originals = payload.filter((item) => existsSync(join(root, item)));
try {
  writeFileSync(
    join(backupRoot, "owned.json"),
    JSON.stringify({ version: 1, originals }),
  );
} catch (error) {
  chmodSync(backupRoot, 0o700);
  const marker = join(backupRoot, "owned.json");
  if (existsSync(marker)) unlinkSync(marker);
  try {
    rmdirSync(backupRoot);
  } catch (cleanupError) {
    if (cleanupError.code !== "ENOTEMPTY" && cleanupError.code !== "EEXIST") {
      throw cleanupError;
    }
  }
  throw error;
}
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
