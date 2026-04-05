#!/usr/bin/env node
const { spawnSync } = require("node:child_process");
const path = require("node:path");

const repoRoot = path.resolve(__dirname, "..");
const installer = path.join(repoRoot, "installer.py");
const args = process.argv.slice(2);

const finalArgs = args.length === 0 ? ["install"] : args;
const result = spawnSync("python3", [installer, ...finalArgs], {
  stdio: "inherit",
});

if (result.error) {
  console.error("Failed to start python3 for MeOS installer.");
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status ?? 1);
