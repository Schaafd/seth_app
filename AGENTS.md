# Repository Guidelines

## Project Structure & Module Organization
Punnyland ships as a Python package in `punnyland/`, with Click commands defined in `cli.py` and shared presentation helpers in `ui.py`. Joke retrieval and enrichment live in `jokes.py`, backed by the curated dataset in `punnyland/data/jokes.json`. Long-term user preferences, history, and favorites are managed through `user.py`, which persists data in `~/.punnyland/`. Keep assets such as ASCII art alongside their consuming modules, and place any new developer utilities at the repo root so they stay out of the runtime package.

## Build, Test, and Development Commands
Use `uv` for dependency management: `uv sync` installs runtime packages declared in `pyproject.toml`, while `uv sync --group dev` pulls in the pytest toolchain. Run the CLI locally with `uv run punnyland joke --level 3` or explore the full menu via `uv run punnyland --help`. QA: `uv run punnyland interactive`. For editable installs, run `pip install -e .` inside a venv that already has the base dependencies.

## Coding Style & Naming Conventions
Follow standard PEP 8 guidelines: four-space indentation, snake_case for functions and variables, and CapWords for classes. Keep public Click commands thin and push business logic into reusable helpers so the CLI remains declarative. Type hints are encouraged for any new functions that cross module boundaries, especially when they pass joke payloads or user state.

## Testing Guidelines
The repository does not yet include automated tests, so new features should introduce `pytest` coverage under a top-level `tests/` directory. Mirror the CLI flows by exercising command callbacks with Click's testing utilities, and include representative fixtures for each corniness level. Run suites with `uv run pytest`; the dev dependency group already includes `pytest-cov`, so coverage runs like `uv run pytest --cov=punnyland` should pass without extra setup.

## Commit & Pull Request Guidelines
Commits follow a light Conventional Commits style (`feat:`, `fix:`, `chore:`) as seen in the existing history. Keep messages in the imperative voice and scoped to a single change. Pull requests should describe user-visible behavior, note any data migrations touching `~/.punnyland/`, and include before/after terminal captures when UI output changes. Link issues where applicable and call out follow-up ideas in a dedicated "Next Steps" paragraph.

## Configuration & Data Tips
Respect user data stored in `~/.punnyland/`; migrations must be idempotent and always back up existing files (see `jokes.json.backup` for precedent). When expanding the joke catalog, keep the JSON alphabetized by punchline to limit merge conflicts.
