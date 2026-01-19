#!/bin/bash
#
# mduck Installation & Update Script
#
# This script will install or update the mduck service using Docker Compose.
# It is designed for Linux, macOS, and Windows (via WSL).
#
# GitHub: https://github.com/aatrubilin/mduck
#

# ---
# Colors and formatting
# ---
C_RESET='\033[0m'
C_RED='\033[0;31m'
C_GREEN='\033[0;32m'
C_BLUE='\033[0;34m'
C_BOLD='\033[1m'

# ---
# Helper Functions
# ---
info() {
    echo -e "${C_BLUE}${C_BOLD}INFO:${C_RESET} $1"
}

success() {
    echo -e "${C_GREEN}${C_BOLD}SUCCESS:${C_RESET} $1"
}

error() {
    echo -e "${C_RED}${C_BOLD}ERROR:${C_RESET} $1" >&2
    exit 1
}

# ---
# Main Script Logic
# ---
main() {
    # ---
    # 1. System and OS Check
    # ---
    info "Checking system compatibility..."
    if [[ "$OSTYPE" != "linux-gnu"* && "$OSTYPE" != "darwin"* ]]; then
        error "This script is intended for Linux, macOS, or Windows Subsystem for Linux (WSL). Your OS '$OSTYPE' is not supported."
    fi
    success "System compatibility check passed."

    # ---
    # 2. Docker prerequisites check
    # ---
    info "Checking for Docker..."
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker before running this script. See: https://docs.docker.com/get-docker/"
    fi

DOCKER_VERSION=$(docker version --format '{{.Server.Version}}')
MIN_DOCKER_VERSION="20.10.0"
if [[ "$(printf '%s\n' "$MIN_DOCKER_VERSION" "$DOCKER_VERSION" | sort -V | head -n1)" != "$MIN_DOCKER_VERSION" ]]; then
        error "Your Docker version is $DOCKER_VERSION. Version $MIN_DOCKER_VERSION or higher is required. Please update Docker."
    fi

    if ! docker compose version &> /dev/null; then
        error "Docker Compose is not available. Please ensure it is installed and accessible."
    fi
    success "Docker and Docker Compose are installed and meet the version requirements."

    # ---
    # 3. Installation Directory
    # ---
    info "Setting up installation directory..."
    DEFAULT_DIR="$HOME/mduck"
    read -p "Enter installation directory [default: $DEFAULT_DIR]: " INSTALL_DIR
    INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_DIR}

mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR" || error "Could not create or switch to directory: $INSTALL_DIR"
    success "Installation directory set to: $INSTALL_DIR"

    # ---
    # 4. Download configuration files
    # ---
    info "Downloading latest configuration files..."
    REPO_URL="https://raw.githubusercontent.com/aatrubilin/mduck/master"
    curl -fsSL "$REPO_URL/compose.yml" -o "compose.yml" || error "Failed to download compose.yml"
    curl -fsSL "$REPO_URL/.env.example" -o ".env.example" || error "Failed to download .env.example"
    success "Configuration files downloaded."

    # ---
    # 5. Configure .env file
    # ---
    info "Configuring environment..."
    if [ ! -f ".env" ]; then
        info "'.env' file not found. Creating a new one from the example."
        cp .env.example .env

        info "Please provide your Telegram Bot Token."
        while true; do
            read -p "Enter TG__TOKEN: " TG_TOKEN
            if [ -n "$TG_TOKEN" ]; then
                sed -i.bak "s|TG__TOKEN=.*|TG__TOKEN=$TG_TOKEN|" .env
                break
            else
                echo -e "${C_RED}Token cannot be empty. Please try again.${C_RESET}"
            fi
        done

        info "Please provide the public webhook host for your bot (e.g., https://your-domain.com)."
        while true; do
            read -p "Enter TG__WEBHOOK__HOST: " TG_WEBHOOK_HOST
            if [ -n "$TG_WEBHOOK_HOST" ]; then
                sed -i.bak "s|TG__WEBHOOK__HOST=.*|TG__WEBHOOK__HOST=$TG_WEBHOOK_HOST|" .env
                break
            else
                echo -e "${C_RED}Webhook host cannot be empty. Please try again.${C_RESET}"
            fi
        done
        rm .env.bak
        success "'.env' file created and configured with your essential variables."
        info "You can edit the '.env' file later to customize other settings."
    else
        success "Existing '.env' file found. Skipping interactive configuration."
    fi

    # ---
    # 6. Start/Update the service
    # ---
    info "Pulling the latest Docker images..."
    docker compose pull || error "Failed to pull Docker images."

    info "Starting the mduck service..."
    docker compose up -d --remove-orphans || error "Failed to start the service."

    info "Cleaning up old images..."
    docker image prune -f

    success "The mduck service has been successfully installed/updated and is running in the background."
}

# ---
# Run main function
# ---
main "$@"
