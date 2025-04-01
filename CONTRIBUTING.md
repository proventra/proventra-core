# Contributing to ProventraCore

We love your input! We want to make contributing to ProventraCore as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Environment

### Using uv (Recommended)

We recommend using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver written in Rust:

```bash
# Install uv (if not already installed)
pip install uv

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies with uv
uv pip install -e ".[all,dev]"
```

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -e ".[all,dev]"`)
4. Make changes and add tests if applicable
5. Run tests (`pytest`)
6. Format your code (example below)
7. Commit your changes (`git commit -m 'Add some amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Pull Requests

1. Update the README.md with details of changes if applicable
2. Update the version number in src/proventra_core/__init__.py following [SemVer](http://semver.org/)
3. The PR will be merged once you have the sign-off of a maintainer

## Code Style

We use several tools to maintain code quality:

- [Ruff](https://docs.astral.sh/ruff/) for code linting and formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [mypy](http://mypy-lang.org/) for static type checking

Our CI workflow runs these tools automatically on all PRs.

### Running Code Quality Checks Locally

Before submitting a PR, run the following command to check your code meets our quality standards:

```bash
# Format code
uv run ruff format src tests examples && \
uv run isort src tests examples && \
# Lint and type check
uv run ruff check src tests examples && \
uv run mypy src && \
# Run tests
uv run pytest
```

For a quick check without modifying your code:

```bash
# Check only - no modifications
uv run ruff format --check src tests examples && \
uv run isort --check-only src tests examples && \
uv run ruff check src tests examples && \
uv run mypy src && \
uv run pytest
```

## Testing

We use [pytest](https://docs.pytest.org/) for testing. Please write tests for new code you create and run the test suite before submitting a PR:

```bash
uv run pytest
```

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License. 