# Dagster Docker Compose Deployment

A complete, production-ready Dagster setup using Docker Compose.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐    ┌──────────────────┐              │
│  │  dagster_webserver│    │  dagster_daemon  │              │
│  │  (UI on :3000)   │    │  (schedules,     │              │
│  │                  │    │   sensors, queue)│              │
│  └────────┬─────────┘    └────────┬─────────┘              │
│           │                       │                         │
│           └───────────┬───────────┘                         │
│                       │                                     │
│                       ▼                                     │
│           ┌──────────────────┐                              │
│           │   dagster_code   │                              │
│           │  (gRPC server    │                              │
│           │   on :4000)      │                              │
│           └────────┬─────────┘                              │
│                    │                                        │
│                    ▼                                        │
│           ┌──────────────────┐                              │
│           │  PostgreSQL      │                              │
│           │  (metadata DB)   │                              │
│           └──────────────────┘                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
dagster-docker-demo/
├── docker-compose.yml          # Container orchestration
├── dagster.yaml                # Dagster instance config
├── workspace.yaml              # Code location config
├── requirements.txt            # Python dependencies
├── Makefile                    # Convenience commands
├── docker/
│   └── Dockerfile             # Container image
└── dagster_project/           # Your pipeline code
    ├── __init__.py            # Definitions entry point
    ├── assets.py              # Software-defined assets
    ├── jobs.py                # Job definitions
    ├── schedules.py           # Time-based triggers
    ├── sensors.py             # Event-based triggers
    └── resources.py           # Shared infrastructure
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- 4GB+ RAM available

### 1. Start the Stack

```bash
# Build and start all services
docker compose up --build -d

# View logs
docker compose logs -f
```

### 2. Access the UI

Open http://localhost:3000 in your browser.

### 3. Run Your First Pipeline

1. Go to **Assets** in the left sidebar
2. Click **Materialize all** in the top right
3. Watch the run progress in the **Runs** tab

### 4. Stop the Stack

```bash
docker compose down

# To also remove volumes (database data):
docker compose down -v
```

## 📋 Common Commands

```bash
# Start in background
docker compose up -d

# Rebuild after code changes
docker compose up --build -d

# View logs
docker compose logs -f dagster_webserver
docker compose logs -f dagster_daemon
docker compose logs -f dagster_code

# Restart a specific service
docker compose restart dagster_code

# Shell into a container
docker compose exec dagster_code bash

# Check status
docker compose ps
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file to override defaults:

```env
# Database
DAGSTER_POSTGRES_USER=dagster
DAGSTER_POSTGRES_PASSWORD=your_secure_password
DAGSTER_POSTGRES_DB=dagster

# Application
DATABASE_HOST=your_app_db_host
DATABASE_USER=your_app_user
API_KEY=your_api_key
```

### Adding New Dependencies

1. Add to `requirements.txt`
2. Rebuild: `docker compose up --build -d`

### Adding Integrations

Popular Dagster integrations:

```txt
# Add to requirements.txt

# dbt integration
dagster-dbt

# Cloud storage
dagster-aws
dagster-gcp
dagster-azure

# Databases
dagster-snowflake
dagster-databricks

# Orchestration
dagster-airflow  # migrate from Airflow
dagster-k8s      # Kubernetes job launcher
```

## 🏭 Production Considerations

### Security

1. **Change default passwords** in `.env`
2. **Use secrets management** (Docker secrets, Vault, etc.)
3. **Enable HTTPS** via reverse proxy (nginx, Traefik)
4. **Restrict network access** to the UI

### Scaling

For production workloads, consider:

1. **Kubernetes** - Use the Helm chart for auto-scaling
2. **Separate run workers** - Use `DockerRunLauncher` or `K8sRunLauncher`
3. **External PostgreSQL** - Use managed database (RDS, Cloud SQL)
4. **Object storage** - Store logs/artifacts in S3/GCS

### Run Launcher Options

Update `dagster.yaml` for Docker-based run isolation:

```yaml
run_launcher:
  module: dagster_docker
  class: DockerRunLauncher
  config:
    image: your-dagster-image:latest
    network: dagster_network
```

### Monitoring

- **Health checks**: Already configured in docker-compose.yml
- **Metrics**: Enable StatsD or Prometheus exporters
- **Alerts**: Configure alert policies in Dagster or external tools

## 🔍 Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs dagster_webserver

# Common fix: wait for postgres
docker compose restart dagster_webserver
```

### Code changes not reflected

```bash
# Rebuild the code server
docker compose up --build dagster_code -d

# Then reload the workspace in UI (Deployment > Reload)
```

### Database connection errors

```bash
# Check postgres is healthy
docker compose ps

# Check connectivity
docker compose exec dagster_code pg_isready -h dagster_postgresql -U dagster
```

### Permission errors

```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./data
```

## 📚 Next Steps

1. **Add your own assets** in `dagster_project/assets.py`
2. **Configure schedules** for automated runs
3. **Set up sensors** to react to external events
4. **Add integrations** for your data sources
5. **Explore partitions** for time-based data processing

## 📖 Resources

- [Dagster Documentation](https://docs.dagster.io)
- [Dagster GitHub](https://github.com/dagster-io/dagster)
- [Dagster Slack Community](https://dagster.io/slack)
