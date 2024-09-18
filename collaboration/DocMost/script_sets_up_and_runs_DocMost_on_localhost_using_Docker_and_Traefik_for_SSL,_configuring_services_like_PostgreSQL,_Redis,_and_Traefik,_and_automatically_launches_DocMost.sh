#!/bin/ 
# Script to install and run DocMost with Docker and Traefik on localhost

# Step 1: Create directories for DocMost
echo "Creating necessary directories for DocMost"
mkdir -p ~/docmost/certs
chmod 600 ~/docmost/certs
cd ~/docmost

# Step 2: Download Docker Compose file for DocMost
echo "Downloading Docker Compose file for DocMost"
curl -O https://raw.githubusercontent.com/docmost/docmost/main/docker-compose.yml

# Step 3: Configure Docker Compose for localhost
echo "Configuring Docker Compose file for localhost"
cat <<EOL > docker-compose.yml
version: '3'

services:
  docmost:
    image: docmost/docmost:latest
    depends_on:
      - db
      - redis
    environment:
      APP_URL: 'http://localhost:3000'
      APP_SECRET: '$(openssl rand -hex 32)'
      DATABASE_URL: 'postgre ://docmost:password@db:5432/docmost?schema=public'
      REDIS_URL: 'redis://redis:6379'
    ports:
      - '3000:3000'
    restart: unless-stopped
    volumes:
      - docmost:/app/data/storage
    labels:
      - 'traefik.enable=true'
      - 'traefik.http.routers.docmost.rule=Host(`localhost`)'
      - 'traefik.http.services.docmost.loadbalancer.server.port=3000'
      - 'traefik.http.routers.docmost.entrypoints=websecure'
      - 'traefik.http.routers.docmost.tls.certresolver=myresolver'
      - 'traefik.docker.network=web'
    networks:
      - web

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: docmost
      POSTGRES_USER: docmost
      POSTGRES_PASSWORD: password
    restart: unless-stopped
    volumes:
      - db_data:/var/lib/postgre /data
    networks:
      - web

  redis:
    image: redis:7.2-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - web

  traefik:
    restart: unless-stopped
    image: traefik:v3.0
    command:
      - '--api.insecure=true'
      - '--providers.docker=true'
      - '--entrypoints.web.address=:80'
      - '--entrypoints.websecure.address=:443'
      - '--certificatesresolvers.myresolver.acme.tlschallenge=true'
      - '--certificatesresolvers.myresolver.acme.email=admin@localhost'
      - '--certificatesresolvers.myresolver.acme.storage=/certs/acme.json'
      - '--log.level=DEBUG'
    ports:
      - '80:80'
      - '443:443'
      - '8080:8080'
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ~/docmost/certs:/certs
    networks:
      - web

networks:
  web:
    external: true

volumes:
  docmost:
  db_data:
  redis_data:
EOL

# Step 4: Create Docker network
echo "Creating Docker network for Traefik"
docker network create web

# Step 5: Start Docker Compose to run DocMost
echo "Starting Docker Compose for DocMost on localhost"
docker-compose up -d

# Final instructions
echo "DocMost is now installed and running. Access it at http://localhost:3000"
echo "Check Traefik Dashboard at http://localhost:8080/dashboard/ if needed."


gcl 3000
