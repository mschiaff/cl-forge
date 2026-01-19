# Contributing to cl-forge

Thank you for your interest in contributing to `cl-forge`!

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/matias-scht/cl-forge.git
   cd cl-forge
   ```

2. **Install dependencies:**
   We use [uv](https://github.com/astral-sh/uv) for dependency management.
   ```bash
   uv sync --all-groups
   ```

3. **Build the Rust extension:**
   ```bash
   uv run maturin develop
   ```

## Workflow

1. Create a new branch for your feature or bugfix.
2. Implement your changes.
3. Add tests for your changes.
4. Run tests and linting:
   ```bash
   uv run pytest
   uv run ruff check .
   ```
5. Submit a Pull Request.

## Code Style

- We use [Ruff](https://github.com/astral-sh/ruff) for Python linting and formatting.
- Rust code should follow standard `cargo fmt` guidelines.

## License

By contributing to this project, you agree that your contributions will be licensed under the Apache 2.0 License.
