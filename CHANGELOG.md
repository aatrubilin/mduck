# CHANGELOG

<!-- version list -->

## v1.0.0 (2026-01-18)

- Initial Release

### Features

- **Message Queuing & Processing (mduck)**
  - Introduced a message queuing and processing service.
  - Achieved 100% test coverage, including exception handling.

- **Ollama Integration**
  - Added `OllamaRepository` for interacting with the Ollama API.
  - Integrated Ollama into the dependency injection container.
  - Implemented AI-based response generation via Ollama.
  - Added periodic "typing" chat action and Markdown support for richer responses.
  - Refactored to use asynchronous I/O for non-blocking operations.
  - Comprehensive test coverage for all new logic.

- **Telegram Bot Functionality**
  - Added aiogram-based bot with handlers for messages, commands, and new chat members.
  - Implemented both polling and webhook entry points.
  - Integrated with dependency injection and configuration systems.

- **Response Probabilities by Chat Type**
  - `MDuckService` now supports different response probabilities for private, group, and supergroup chats.
  - Unit tests cover all scenarios, including probability edge cases and exceptions.

- **Application Versioning**
  - Added `version.py` to retrieve version from package metadata.
  - Displayed version in FastAPI Swagger UI.

- **Improved Test Coverage**
  - Achieved 100% test coverage across all modules.
  - Fixed all linting issues and warnings.
  - Resolved `RuntimeWarning` for unawaited coroutines in async tests.

- **Project Structure & Config**
  - Added `data/` directory and updated `.gitignore`.
  - Cleaned up import paths and added conventions to documentation.

### Chores

- Added GitHub Actions workflow with semantic-release.
- Configured caching for dependencies.
- Used official `python-semantic-release` GitHub Action.
- Added emojis and descriptive names to workflow steps and jobs.
- Triggered initial semantic release with all fixes in place.
