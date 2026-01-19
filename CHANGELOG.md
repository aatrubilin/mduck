# CHANGELOG

<!-- version list -->

## v1.4.0 (2026-01-19)

### Features

- **ollama**: Add configuration options to ollama service
  ([`a0dee65`](https://github.com/aatrubilin/mduck/commit/a0dee65592001a3a674801bf9d7a5e285386dd4e))


## v1.3.1 (2026-01-19)

### Bug Fixes

- **deploy**: Make install script robust for piped execution
  ([`3688b91`](https://github.com/aatrubilin/mduck/commit/3688b91303e4aced8e594868ff071506a2330483))


## v1.3.0 (2026-01-19)

### Features

- **ci**: Enable multi-architecture docker builds
  ([`190a546`](https://github.com/aatrubilin/mduck/commit/190a54667e5d4f799edc47d75d57d1ee490dafa9))


## v1.2.0 (2026-01-19)

### Features

- **deploy**: Add installation and update script
  ([`712f368`](https://github.com/aatrubilin/mduck/commit/712f368bda519f77f6576ae60f66652f4827fccf))


## v1.1.1 (2026-01-19)

### Bug Fixes

- **ci**: Set up buildx to enable docker layer caching
  ([`add3ed3`](https://github.com/aatrubilin/mduck/commit/add3ed3028cc3c2c715354673a9eff1c877272f9))


## v1.1.0 (2026-01-19)

### Bug Fixes

- **ci**: Install poetry-plugin-export in workflow
  ([`4e42a20`](https://github.com/aatrubilin/mduck/commit/4e42a207398f0296636c469ab1d240d25d56d27f))

- **ci**: Resolve pre-commit hook errors
  ([`4291440`](https://github.com/aatrubilin/mduck/commit/4291440a08690c56b41768e88623a4e59a44c0b6))

- **test**: Resolve hanging test by using AsyncMock
  ([`0ff0f01`](https://github.com/aatrubilin/mduck/commit/0ff0f01e0a4298c4172ff7b2392ec7952d484460))

### Chores

- **build**: Optimize and refactor Dockerfile
  ([`b00a87e`](https://github.com/aatrubilin/mduck/commit/b00a87e2edee7e3bf8f71ea6e88b22894e6f72ce))

- **ci**: Optimize dependency caching in workflow
  ([`93780f9`](https://github.com/aatrubilin/mduck/commit/93780f9fb2ce0f598728de543d5f0acd6167c9c9))

### Documentation

- Update changelog
  ([`ac1a958`](https://github.com/aatrubilin/mduck/commit/ac1a95805e617b1af4837334c27195a969c95036))

### Features

- Implement webhook support and update configuration
  ([`461382b`](https://github.com/aatrubilin/mduck/commit/461382bde3c306d29208050fac3c9c3f2a6f9103))

- **config**: Externalize environment variables with .env
  ([`268af1b`](https://github.com/aatrubilin/mduck/commit/268af1b70b1962c0edd11ab3a409e8a43aa4d1bc))

- **deploy**: Add installation and update script
  ([`df59fe2`](https://github.com/aatrubilin/mduck/commit/df59fe2ed23f0c01a47980fefaf57daa4dae8e66))


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
