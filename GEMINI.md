# Gemini Project: mduck

## Project Overview

This is a Python project named "mduck". It is managed using Poetry for dependency management and packaging. The project's source code is located in the `src/mduck` directory.

This project uses `python-dependency-injector` for dependency injection to manage components and their dependencies.

## Project Structure

The project follows the following structure:

- `src/mduck/containers/*.py`: Dependency-injector containers.
- `src/mduck/repositories/*.py`: Data-access layer.
- `src/mduck/routers/*.py`: API layer with FastAPI routers.
- `src/mduck/schemas/*.py`: Pydantic schemas for data validation and serialization.
- `src/mduck/services/*.py`: Business logic.
- `src/config/settings.py`: Configuration using Pydantic-settings.

## Building and Running

### 1. Install Dependencies

To install the necessary dependencies, run the following command in the project root:

```bash
poetry install
```

### 2. Running the Application

To run the application, use the following command:

```bash
poetry run api --host 0.0.0.0 --port 8000 --reload --log-level info
```

### 3. Running Tests

To run tests and check coverage, use:

```bash
poetry run pytest --cov=src/mduck
```

## Development Conventions

*   All Python source code should be placed within the `src/mduck` directory.
*   Tests should be placed in the `tests/` directory. The structure of the `tests` directory should mirror the `src/mduck` directory.
*   **Dependencies**
    Dependencies are managed via the `pyproject.toml` file. To add a new dependency, use:
    ```bash
    poetry add <package-name>
    ```
    For development-only dependencies, use:
    ```bash
    poetry add --group dev <package-name>
    ```

*   **Import Paths**
    When importing modules, treat the `src` directory as the project root. For example, to import `settings` from `src/config/settings.py`, use `from config.settings import settings`. Similarly, for modules within `src/mduck`, use `from mduck.<module> import ...`. Do not prefix imports with `src.`.

*   **Commit Messages**
    This project follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. All commit messages should adhere to this format.

*   **Type Annotations**
    All code must use type annotations wherever possible, including function arguments, return values, and class attributes. This is enforced by `mypy`.

*   **Linting and Formatting**
    To lint and format the code using `ruff`:
    ```bash
    poetry run ruff check src/mduck tests
    poetry run ruff format src/mduck tests
    ```

*   **Type Checking**
    To perform static type checking using `mypy`:
    ```bash
    poetry run mypy --strict src/mduck
    ```
