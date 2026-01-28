# CHANGELOG

<!-- version list -->

## v1.14.0 (2026-01-28)

### Chores

- **ci**: Update coverage badge
  ([`98128b9`](https://github.com/aatrubilin/mduck/commit/98128b951d7cc457cf7db4d18f379c37b3bc3446))

### Features

- Add comprehensive tests for MDuckService
  ([`1c8d81d`](https://github.com/aatrubilin/mduck/commit/1c8d81dda9937c3ea92479ddded097096437e904))

- Add tests for webhook and whoami routers
  ([`e6ca554`](https://github.com/aatrubilin/mduck/commit/e6ca554ba9f510a886037e9dd70e75b8d1416820))

### Refactoring

- Improve test suite consistency and reduce redundancy
  ([`d764ee0`](https://github.com/aatrubilin/mduck/commit/d764ee02f26dfc568c25b8ed80b8442fa6db2b99))

### Testing

- Add unit test for chat_member handler
  ([`e13dc7d`](https://github.com/aatrubilin/mduck/commit/e13dc7d5a1f3c0498d957430df1a6ef189f87cfa))


## v1.13.0 (2026-01-27)

### Chores

- **deps-dev**: Bump the python-dependencies group with 3 updates
  ([`3b286a0`](https://github.com/aatrubilin/mduck/commit/3b286a00bb73a43bc38a06703258cd9a4d47bb98))

### Features

- Configure Dependabot to widen versioning strategy
  ([`480865d`](https://github.com/aatrubilin/mduck/commit/480865d25464b8b56411c54ca6dad4745dc7e679))


## v1.12.0 (2026-01-27)

### Chores

- **deps**: Bump the github-actions-dependencies group with 4 updates
  ([`bf311f6`](https://github.com/aatrubilin/mduck/commit/bf311f6241e6a7cc42e9c303a95e420d883d29ac))

### Features

- Add Dependabot for dependency management
  ([`5e9cd94`](https://github.com/aatrubilin/mduck/commit/5e9cd9485228c06d29b2ab58b5379a41abe7bcd4))


## v1.11.0 (2026-01-24)

### Chores

- **ci**: Update coverage badge
  ([`d6ca7be`](https://github.com/aatrubilin/mduck/commit/d6ca7bec24e198e1ffaf9dae3a1afcec34f87515))

### Features

- Add and refine prompt examples, introduce new personas
  ([`d726b05`](https://github.com/aatrubilin/mduck/commit/d726b05cf4200476bf01cab0df2306368eb37467))

- Fix context propagation and refine Ollama integration
  ([`f28cbb3`](https://github.com/aatrubilin/mduck/commit/f28cbb3d539aff66a3ff129ded8767943261186d))

- **ollama**: Enhance Ollama response handling and metadata
  ([`c94ad56`](https://github.com/aatrubilin/mduck/commit/c94ad5635d2c94fe61e21895bc62a084be4962b3))

- **ollama**: Update Ollama Docker image to alpine/ollama:0.12.10
  ([`b6be51e`](https://github.com/aatrubilin/mduck/commit/b6be51ed6cc00c9c3bd950667ded475fcc3097fb))

### Refactoring

- **ollama**: Load system prompts from a directory
  ([`cfc68e0`](https://github.com/aatrubilin/mduck/commit/cfc68e0de33d39477a3eadf02784d6e0c7bf7583))

- **ollama**: Use pathlib.Path for prompt loading
  ([`fe8d7ca`](https://github.com/aatrubilin/mduck/commit/fe8d7ca9bab29b8987b94fb886048447621d5e1c))


## v1.10.5 (2026-01-21)

### Bug Fixes

- Prompts
  ([`46fd19d`](https://github.com/aatrubilin/mduck/commit/46fd19db99f3ae1c6ec18f5f6e61a6010c700c7c))


## v1.10.4 (2026-01-21)

### Bug Fixes

- Proxy-headers
  ([`d0be903`](https://github.com/aatrubilin/mduck/commit/d0be9033bef5c51ab64b86472f1665f258027081))


## v1.10.3 (2026-01-21)

### Bug Fixes

- Increase typing interval sending
  ([`fd2462e`](https://github.com/aatrubilin/mduck/commit/fd2462e742394d6d60f264a95a54fac2875fa6dc))

- Logging prompts
  ([`87b745e`](https://github.com/aatrubilin/mduck/commit/87b745ed1247ed04427c87820e79b459afda041d))

### Documentation

- Specify model used for Raspberry Pi testing
  ([`1e362b9`](https://github.com/aatrubilin/mduck/commit/1e362b92c8bae571daf40eeb9cfb52af94c80ff5))


## v1.10.2 (2026-01-21)

### Bug Fixes

- Ensure context propagation for typing indicator task
  ([`c1c0455`](https://github.com/aatrubilin/mduck/commit/c1c04556593edbbf684155911595cc6abb3bd6ce))

- Peotry lock
  ([`7c00dcf`](https://github.com/aatrubilin/mduck/commit/7c00dcfe9918b06c15e6b4455dfcd476ac5da566))

- **ci**: Correct genbadge command for coverage badge
  ([`a6408a8`](https://github.com/aatrubilin/mduck/commit/a6408a8e2b78d2210c0041a1c66816e2ef1cacd0))

- **ci**: Fix coverage badge generation
  ([`783709d`](https://github.com/aatrubilin/mduck/commit/783709de2ccf6ab2192ffa42e06f8ea5661afa5d))

- **ci**: Grant write permissions to commit coverage badge
  ([`c7b490b`](https://github.com/aatrubilin/mduck/commit/c7b490bef324692a1c55d6078dc059d20d2519d6))

- **ci**: Synchronize with remote before release
  ([`138b455`](https://github.com/aatrubilin/mduck/commit/138b455cd1dbaf2b6c29e68a9879af7a9ebb510d))

- **deps**: Update poetry.lock for genbadge[coverage]
  ([`8533681`](https://github.com/aatrubilin/mduck/commit/8533681acd47d6f16c5ac0ddbfb2dd0f53194fdd))

### Chores

- Add .gemini/ to .gitignore
  ([`a19197a`](https://github.com/aatrubilin/mduck/commit/a19197a5b897f0d78d791bf51f7878d3e90f816b))

- **ci**: Update coverage badge
  ([`bf5cde0`](https://github.com/aatrubilin/mduck/commit/bf5cde078cd10bf5824c9586fdf1712de925f122))

### Continuous Integration

- Add test coverage reporting with Codecov
  ([`8c4ced5`](https://github.com/aatrubilin/mduck/commit/8c4ced5ac3e0bda573a305425db58bac4de865e9))

### Documentation

- Add license and new badges to README
  ([`1464898`](https://github.com/aatrubilin/mduck/commit/1464898e0cec8855ce80e7ff213808632f80a035))

- Add license and new badges to README
  ([`619f90f`](https://github.com/aatrubilin/mduck/commit/619f90f712dcec6678609f88478d04be9cd535ba))

- Enhance README with logo, bot link, and RPi compatibility
  ([`adffcf9`](https://github.com/aatrubilin/mduck/commit/adffcf936e83ec49c846375f3ac8196240dcfb01))


## v1.10.1 (2026-01-21)

### Bug Fixes

- Remove usertag from message
  ([`09dca8a`](https://github.com/aatrubilin/mduck/commit/09dca8a157713fb2ddba4f44b3577a6172fd02b9))

- **install**: Improve error handling and fix duplicated code in install script
  ([`ffef90a`](https://github.com/aatrubilin/mduck/commit/ffef90af484bf444afc7d54a575bff6127b81c9b))

### Refactoring

- **docker**: Streamline dependency installation in Dockerfile
  ([`ffef90a`](https://github.com/aatrubilin/mduck/commit/ffef90af484bf444afc7d54a575bff6127b81c9b))


## v1.10.0 (2026-01-21)

### Bug Fixes

- Propagate context to background processor
  ([`46207a7`](https://github.com/aatrubilin/mduck/commit/46207a7439e0423e43504c952fc2aa071be4e0ae))

### Features

- Add forwarded_allow_ips to uvicorn config
  ([`52b6d5c`](https://github.com/aatrubilin/mduck/commit/52b6d5cf2abec5d61bcaefb2b69d2b710b11b464))


## v1.9.0 (2026-01-21)

### Features

- Implement message queue size limit
  ([`1cee232`](https://github.com/aatrubilin/mduck/commit/1cee232f149f2ae4293462b2ab3b75199c802044))


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
