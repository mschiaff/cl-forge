---
name: contextual-commit-messages
description: Compose Conventional Commits grounded in staged and unstaged git changes plus the cl-forge project context. Use when Codex must craft a commit message that follows the Conventional Commits spec and RFC 2119 requirements for this repository.
---

# Contextual Commit Messages

## Overview

Create Conventional Commit messages that accurately represent the actual work in progress. The workflow enforces that the summary is derived from **both staged and unstaged changes**, reflects how the change impacts cl-forge's Rust/Python toolchain, and uses RFC 2119 wording whenever you describe requirements or follow-up actions inside the commit body.

## Quick Workflow

1. Build context: read `README.md`, `Cargo.toml`, `pyproject.toml`, or touched docs/tests to understand the feature surface being changed.
2. Inspect the working tree with `git status -sb`, `git diff --staged`, and `git diff` so you know exactly what is committed vs. remaining.
3. Cluster changes into logical units, map them to Conventional Commit `type`/`scope`, and capture any side effects (API, docs, tests, tooling).
4. Draft the subject (`type(scope)!: summary`), add a wrapped body explaining **why** and referencing key files, then add footers for breaking changes/issues/tests.
5. Run the validation checklist before presenting the final message.

## 1. Build Repository Context

- Skim `README.md` plus `docs/` for current positioning: cl-forge is a Chilean data tooling toolkit built primarily in Rust with Python bindings; highlight when commits affect API clients, validators, or publishing workflow.
- Inspect manifest files to identify scopes:
  - `Cargo.toml` / `src/` for Rust crates (`cl-forge-core`, `cl-forge-ffi`, etc.).
  - `pyproject.toml`, `src/cl_forge/`, and `tests/` for Python packaging and stubs.
  - `docs/` or `site/` for mkdocs outputs.
- When diffs touch configuration (CI, release scripts), read `.github/workflows/` or `release.sh` to confirm intended automation.
- Prefer scopes that align with directories, crates, or high-level capabilities (e.g., `verify`, `cmf`, `market`, `docs`, `ci`).

## 2. Inspect Git State (MUST)

- Run `git status -sb` to see staged (`A/M`) vs unstaged (`??`, ` M`). Never assume what is staged; always verify.
- Capture snapshots while writing:
  - `git diff --staged` for the exact commit content.
  - `git diff` (no flags) for unstaged work so you understand the developer's intent even if it is not included yet. Mention unstaged dependencies if they block the commit.
  - `git diff --stat` to quickly size the change and decide if multiple commits are warranted.
- When staged work depends on unstaged files, either block on staging them or clearly flag the dependency inside the commit body using RFC 2119 terms (e.g., "Tests MUST be updated before release").

## 3. Classify Change Type, Scope, and Impact

- **Type selection (MUST follow Conventional Commits):** `feat`, `fix`, `docs`, `refactor`, `chore`, `perf`, `test`, `build`, `ci`, `revert`. Pick the one describing the user-visible impact; default to `chore` only when no other type applies.
- **Scope (SHOULD be provided):** derive from directory/crate/module touched. Keep it short (`verify`, `cmf-client`, `docs`, `ci`). Use `*` only when multiple independent areas change.
- **Breaking changes:** if APIs alter runtime behavior or signature, append `!` and describe the consequence in the body plus a `BREAKING CHANGE:` footer.
- **Documentation + tests:** note when docs/tests were added or MUST still be added; use RFC 2119 verbs (`SHOULD add regression tests covering ...`).

## 4. Draft the Message

- **Subject line:** `type(scope)!: imperative summary`
  - Keep <= 72 characters, describe the effect ("add CMF IPC pagination guard").
  - Never end with a period; do not mention files or ticket IDs here.
- **Body paragraphs (wrap at 72 columns):**
  - First paragraph explains *why* the change exists referencing evidence from diffs (benchmarks, bug reproduction, API requirements).
  - Subsequent paragraphs MAY outline implementation details, trade-offs, or follow-ups. Use bullet lists for multi-point explanations.
  - Reference unstaged work if relevant ("Unstaged `tests/test_market.py` updates MUST land before release to keep CI green.").
- **Footers:**
  - `BREAKING CHANGE: ...` when behavior or API contracts change.
  - `Refs: #123`, `Related-to: Docs build pipeline`, or `Co-authored-by` entries when applicable.
  - Mention testing evidence (`Tests: pytest tests/verify`) so reviewers understand coverage.

### Template

```
type(scope)!: concise subject

Motivation paragraph explaining the user/technical problem.
Implementation + context paragraph(s), referencing staged files and
calling out any unstaged dependencies using RFC 2119 verbs.

Tests: <command>
BREAKING CHANGE: <details> (only when applicable)
Refs: <issue links>
```

## 5. Validate Before Sharing

- Subject MUST follow Conventional Commits syntax and highlight the real scope.
- All sentences referencing obligations MUST use RFC 2119 verbs (MUST, SHOULD, MAY, etc.). Avoid casual "need to".
- Verify the message still matches `git diff --staged` after any last-minute edits.
- Ensure wrapped width <= 72 characters for body/footers.
- Double-check that referenced unstaged work is either staged or explicitly documented as pending.

## Reference Material

- Load `references/spec-quick-reference.md` for a condensed checklist of Conventional Commits semantics, RFC 2119 definitions, and worked examples tailored to cl-forge.
