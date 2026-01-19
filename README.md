[![Made with Gemini](https://img.shields.io/badge/Made%20with-Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://gemini.google.com)


![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/aatrubilin/mduck/release.yml)
![GitHub Release](https://img.shields.io/github/v/release/aatrubilin/mduck)

# MooDuck Bot `mduck`

A caustic Telegram bot service.

## Overview

This project implements a Telegram bot service designed to generate sarcastic and caustic comments in response to chat messages. Leveraging Ollama for natural language processing, the bot aims to provide "spicy" remarks, adding a unique flavor to group conversations.

## Installation

### One-Liner Install (Linux, macOS, WSL)

To install or update the `mduck` service, run the following command in your terminal. The script will guide you through the process.

```bash
curl -fsSL https://raw.githubusercontent.com/aatrubilin/mduck/master/install.sh | sh
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
