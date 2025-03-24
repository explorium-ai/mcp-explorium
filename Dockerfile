FROM python:3.11-slim

ARG WORKDIR=/app
WORKDIR ${WORKDIR}

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="${WORKDIR}/.venv/bin:$PATH" \
    PYTHONPATH="${WORKDIR}" \
    SHELL="/bin/bash" \
    PNPM_HOME="/root/.local/share/pnpm"

ENV PATH="/root/.local/share/pnpm:$PATH"

# Install Node.js and npm for the React UI
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    wget \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm

# Install Python tools
RUN pip install uv

# Copy source code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir langgraph
RUN uv sync --frozen --group agent

# Pre-install pnpm dependencies and build agent-ui
RUN cd /app/agent-ui && pnpm install && pnpm build

# Install serve for hosting the UI
RUN npm install -g serve

# Expose ports
EXPOSE 5175 2024

# Create and set up entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Default app type
ENV APP_TYPE=mcp

ENTRYPOINT ["/docker-entrypoint.sh"]

