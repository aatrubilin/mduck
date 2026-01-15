# MooDuck Bot (`mduck`)

A caustic Telegram bot service.

## Overview

This project implements a Telegram bot service designed to generate sarcastic and caustic comments in response to chat messages. Leveraging Ollama for natural language processing, the bot aims to provide "spicy" remarks, adding a unique flavor to group conversations.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. Ensure you have it installed before proceeding.

### Installation

Clone the repository and install the required dependencies using Poetry:

```bash
poetry install
```

### Running the Application

To run the application locally, use the following command:

```bash
poetry run api --host 0.0.0.0 --port 8000 --reload --log-level info
```

The application will be available at `http://0.0.0.0:8000`. The `--reload` flag enables hot-reloading for development.

## Development

This entire project was developed using a "vibecoding" approach with the assistance of Gemini, emphasizing rapid prototyping and iterative development.
