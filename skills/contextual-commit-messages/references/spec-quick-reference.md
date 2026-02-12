# Conventional Commits + RFC 2119 Quick Reference

## Required Message Shape

```
type(scope)!: subject (imperative, <= 72 chars)

<Body paragraphs wrapped at 72 cols>

<Footers>
```

- `type` (lowercase) MUST be one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- `scope` SHOULD highlight the primary area (directory/crate/module). Drop the parentheses only when omitting the scope entirely.
- Append `!` when introducing a breaking change; explain the impact and migration in the body and in a `BREAKING CHANGE:` footer.
- Keep the subject imperative and avoid trailing punctuation.

## RFC 2119 Vocabulary

Use these verbs to describe requirements inside the body/footers:

| Term  | Meaning                                                                 |
|-------|-------------------------------------------------------------------------|
| MUST / MUST NOT | Absolute requirement. Use when CI will break or APIs fail without the follow-up. |
| SHOULD / SHOULD NOT | Strong recommendation; valid reasons MAY exist to ignore, but highlight consequences. |
| MAY  | Optional behavior or follow-up.                                          |
| REQUIRED | Another form of MUST when you are listing prerequisites.            |
| OPTIONAL | Equivalent to MAY.                                                   |

Avoid soft language such as "need to" or "nice to"; pick one of the above to keep the message unambiguous.

## Context Checklist for cl-forge

- `src/` and `rust/` folders map to Rust crates; treat each as its own possible scope.
- Python bindings live under `src/cl_forge/` with typing stubs in `src/cl_forge/py.typed`; call out packaging or typing fixes explicitly.
- Docs are built via mkdocs (`mkdocs.yml`, `docs/`, `site/`); doc-only commits SHOULD use `docs(scope): ...`.
- Release automation touches `release.sh`, `docs.sh`, `.github/workflows/*`, and `pyproject.toml`; these often require `build` or `ci` types.

## Example Messages

```
feat(market)!: enforce authenticated tender lookups

Mercado Publico APIs now reject anonymous pagination, so the Rust
client enforces ticket injection and raises a typed error when the
server responds with 401. This keeps the python bindings consistent
with the new SLA and documents the breaking behavior.

Docs: mkdocs build
Tests: cargo test -p market-client
BREAKING CHANGE: Unauthenticated lookups now raise MarketAuthError.
```

```
chore(ci): gate release workflow on universal wheels

Identify missing universal wheels during release builds and fail fast.
Unstaged tests SHOULD cover `release.sh --check` before publishing to
PyPI to avoid partial uploads.

Refs: #456
```
