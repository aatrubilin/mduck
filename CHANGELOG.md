# CHANGELOG

<!-- version list -->

## v1.8.0 (2026-01-21)

### Features

- Add /whoami endpoint and improve typing indicator
  ([`b9fbe32`](https://github.com/aatrubilin/mduck/commit/b9fbe32c10772032454ff9c84aff75ddfbcee551))


## v1.7.1 (2026-01-21)

### Bug Fixes

- Dependency injector wiring
  ([`a983cc3`](https://github.com/aatrubilin/mduck/commit/a983cc39b2d9e561a27ab5a67c7cb0067d600da3))

### Refactoring

- **compose**: Use YAML anchor to reduce duplication
  ([`231c6aa`](https://github.com/aatrubilin/mduck/commit/231c6aa798e902bb40488ac45e80a1291776b4ad))


## v1.7.0 (2026-01-21)

### Features

- Improve reply handling and context
  ([`67bea87`](https://github.com/aatrubilin/mduck/commit/67bea874469332991f4037581a576833d7460b40))


## v1.6.0 (2026-01-21)

### Features

- Add healthchecksto compose.yaml
  ([`cdf73a8`](https://github.com/aatrubilin/mduck/commit/cdf73a8d128fa5d481e1e7e8b27c3783ce7389f2))

- Refactor new chat member handling
  ([`a6fd318`](https://github.com/aatrubilin/mduck/commit/a6fd3181f8afa508f030eff02699301e92a2d3fe))


## v1.5.3 (2026-01-21)

### Bug Fixes

- **compose**: Run mduck service as root to fix permission denied error
  ([`da8d022`](https://github.com/aatrubilin/mduck/commit/da8d0228120ae78b9bd92f0fe88ce9fa3d4a1514))


## v1.5.2 (2026-01-21)

### Bug Fixes

- Fixed healthcheck for dockerfile
  ([`e8afb71`](https://github.com/aatrubilin/mduck/commit/e8afb71524a960146862c6c8be6247e0fb3b8f9b))


## v1.5.1 (2026-01-21)

### Bug Fixes

- **compose**: Use wget for ollama healthcheck
  ([`fc748a3`](https://github.com/aatrubilin/mduck/commit/fc748a32fb5223427771b725c9129a388108605d))


## v1.5.0 (2026-01-21)

### Features

- Add file logging and healthchecks
  ([`300a60a`](https://github.com/aatrubilin/mduck/commit/300a60a97d89647d9e4b00019774587820075aa9))

- Improve environment configuration and setup process
  ([`dd21e65`](https://github.com/aatrubilin/mduck/commit/dd21e65bbd3376e011690b1a6d67e6bd9eacf529))

- **logging**: Introduce JSON and human-readable log formats
  ([`7d871da`](https://github.com/aatrubilin/mduck/commit/7d871da5640df2f242e3a38c156c03416c06a986))


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
