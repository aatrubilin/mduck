[![Made with Gemini](https://img.shields.io/badge/Made%20with-Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://gemini.google.com)
[![Telegram Bot](https://img.shields.io/badge/tg-@mduckbot-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/mduckbot)


![GitHub last commit](https://img.shields.io/github/last-commit/aatrubilin/mduck)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/aatrubilin/mduck/release.yml)
![GitHub Release](https://img.shields.io/github/v/release/aatrubilin/mduck)

![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-black.svg)](https://github.com/astral-sh/ruff)
![Coverage](assets/coverage.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# MooDuck Bot

This project implements a Telegram bot service designed to generate
sarcastic and caustic comments in response to chat messages.
Leveraging Ollama for natural language processing, the bot aims to provide "spicy" remarks, adding a unique flavor to group conversations.

![MooDuck Logo](assets/mduck-logo.png)

## Tested Environments

This setup is designed to be lightweight and has been successfully tested on low-spec hardware:

-   **Raspberry Pi 5 8GB**: The entire stack, including the bot and the Ollama language model, runs efficiently.

## Installation

### One-Liner Install (Linux, macOS, WSL)

To install or update the `mduck` service, run the following command in your terminal. The script will guide you through the process.

```bash
curl -fsSL https://raw.githubusercontent.com/aatrubilin/mduck/master/install.sh | bash
```

**Note for Windows users**: This command should be run in **WSL (Windows Subsystem for Linux)**.

## Development Setup

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. Ensure you have it installed before proceeding.

### Local Installation

Clone the repository and install the required dependencies using Poetry:

```bash
poetry install
```

### Running the Application

To run the webhook application locally, use the following command:

```bash
poetry run run-webhook --host 0.0.0.0 --port 8000 --reload --log-level info
```

The webhook application will be available at `http://0.0.0.0:8000`. The `--reload` flag enables hot-reloading for development.

To run the pooling application locally, use the following command:

```bash
poetry run run-pooling --reload --log-level debug
```

## Development

This entire project was developed using a "vibecoding" approach with the assistance of [Gemini](https://gemini.google.com), emphasizing rapid prototyping and iterative development.
