# Alignzo Testing Suite Monorepo

This repository contains the complete testing platform for the Alignzo project, designed to manage, execute, and visualize the results of functional, load, and security tests across the Alignzo microservices ecosystem.

## Monorepo Structure

```
.
├── orchestrator/         # FastAPI backend (Test Orchestration Service)
├── frontend/             # React (TypeScript) SPA dashboard
├── runners/              # Test runner containers/scripts
│   ├── functional/
│   ├── load/
│   └── security/
├── db/                   # Database migrations, seed data, schemas
├── scripts/              # Utility scripts (aggregation, notifications, etc.)
├── docker-compose.yml    # For local/dev orchestration
├── .env.example          # Example environment variables
└── .github/
    └── workflows/
        └── ci.yml        # GitHub Actions pipeline
```

## Components

- **orchestrator/**: FastAPI backend for test management, orchestration, and result aggregation.
- **frontend/**: React SPA for dashboards, test management, and result visualization.
- **runners/**: Containerized test runners for functional (Pytest, Playwright), load (k6), and security (ZAP, Trivy) testing.
- **db/**: Database migrations and seed data for the results database.
- **scripts/**: Utility scripts for aggregation, notifications, etc.

## Getting Started

1. Clone the repository.
2. Copy `.env.example` to `.env` and configure environment variables.
3. Use `docker-compose up --build` to start all services locally.
4. Access the frontend dashboard at `http://localhost:3000` (default).

## CI/CD

- Automated via GitHub Actions in `.github/workflows/ci.yml`.

---

For detailed documentation, see the `docs/` folder (to be added).
