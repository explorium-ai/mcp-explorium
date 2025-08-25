FROM node:22-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json ./

# Install dependencies
RUN --mount=type=cache,target=/root/.npm npm ci --only=production

# Copy the rest of the application
COPY server/ ./server/
COPY manifest.json logo.png ./

# Add entrypoint wrapper
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set environment to production
ENV NODE_ENV=production
EXPOSE 44280

# Use wrapper script as entrypoint
ENTRYPOINT ["/entrypoint.sh"]
