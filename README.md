BEGIN
# IMRE: Intelligent Workforce Management Reference Implementation

Event-driven system for shift scheduling and workload aggregation.  
Built with **Clean Architecture**, **Domain-Driven Design**, and **synchronous reliability**.

## High-Level Architecture

```mermaid
graph LR
    A[Client] -->|HTTP/JSON| B["Django API<br>(sync, DRF)"]
    B -->|Read/Write| C[(PostgreSQL)]
    B -->|Publish event| D["Event Handler"]
    D -->|Update aggregates| C
```

✅ No message broker (Redis/Kafka) — synchronous processing ensures simplicity and consistency for MVP.

## Request Flow

```mermaid
flowchart TD
    subgraph Client
        A["POST /api/shifts/"]
        B["GET /api/workload/staff/:id/week/:date"]
    end

    subgraph API_Layer
        A --> C[ShiftCreateView]
        B --> D[WorkloadRetrieveView]
    end

    subgraph Validation_and_Domain
        C --> E[ShiftSerializer<br>staff_id, date, time]
        E -->|Valid| F[wfm_core.Shift<br>validate duration,<br>round to 15min]
        F -->|Invalid| G[400 Bad Request]
        F -->|Valid| H[Create ShiftCreated Event]
    end

    subgraph Event_Processing
        H --> I[handle_shift_created]
        I --> J[Begin DB Transaction]
        J --> K[GetOrCreate WeeklyWorkload<br>staff_id + week_start]
        K --> L[Add duration_hours]
        L --> M[Save WeeklyWorkload]
        M --> N[Commit Transaction]
    end

    subgraph Read_Path
        D --> O[Query WeeklyWorkload<br>by staff_id, week_start]
        O -->|Found| P[200 OK + JSON]
        O -->|Not Found| Q[404 Not Found]
    end

    style A fill:#e6f3ff,stroke:#0066cc
    style B fill:#e6f3ff,stroke:#0066cc
    style C fill:#d4f7e5,stroke:#2e8b57
    style D fill:#d4f7e5,stroke:#2e8b57
    style F fill:#d4f7e5,stroke:#2e8b57
    style I fill:#d4f7e5,stroke:#2e8b57
    style K fill:#d4f7e5,stroke:#2e8b57
    style O fill:#d4f7e5,stroke:#2e8b57
```

## Domain Model (Clean Architecture + DDD)

```mermaid
graph TD
    A[Client] -->|HTTP| B[Django API<br><i>Framework Layer</i>]
    B --> C["wfm_core.Shift<br><i>Entity / Domain</i>"]
    C --> D[(PostgreSQL<br><i>Infrastructure</i>)]
    C -->|event| E["Event Handler<br><i>Application Service</i>"]
    E --> F["WeeklyWorkload Model<br><i>Django ORM → DB</i>"]
    F --> D
    
    style C fill:#d4f7e5,stroke:#2e8b57
    style F fill:#d4f7e5,stroke:#2e8b57
    style B fill:#d4f7e5,stroke:#2e8b57
    style E fill:#d4f7e5,stroke:#2e8b57
    style D fill:#d4f7e5,stroke:#2e8b57
```

✅ **Green = implemented and working**

## Features

- ✅ **Shift creation API** (`POST /api/shifts/`)
  - Validates duration (1–12 hours)
  - Enforces start < end
  - Rounds duration to 15-minute intervals
- ✅ **Workload aggregation** (`GET /api/workload/staff/:id/week/:date`)
  - Stores weekly totals in PostgreSQL
  - ISO week start (Monday)
- ✅ **Event-driven design**
  - `ShiftCreated` event published on success
  - Synchronous processing
- ✅ **Test coverage**
  - Unit tests for domain (`wfm_core`)
  - Integration tests for API
  - End-to-end tests for full flow
- ✅ **Deployment-ready**
  - `render.yaml` included
  - Supports PostgreSQL in production
  - SQLite for local development

## Tech Stack

- **Backend**: Python 3.11, Django 5.0, DRF
- **Domain**: Pure Python (no framework dependencies)
- **Database**: PostgreSQL (production), SQLite (local)
- **Deployment**: Render.com (free tier)
- **Quality**: ruff, pytest, pre-commit

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then:

```bash
# Create a shift
curl -X POST http://localhost:8000/api/shifts/ \
  -H "Content-Type: application/json" \
  -d '{"staff_id": 17, "date": "2026-06-15", "start_time": "09:00", "end_time": "18:00"}'

# Get workload
curl http://localhost:8000/api/workload/staff/17/week/2026-06-15/
```

## Deployment

Live demo: [https://imre-340q.onrender.com](https://imre-340q.onrender.com)

Push to GitHub → auto-deployed to [Render.com](https://render.com).

## Architecture Notes

- **Why synchronous?** Simplicity, atomicity, and debuggability for MVP.
- **Why no Redis?** Avoid operational complexity until needed.
- **Known limitation**: Repeated identical requests will duplicate workload hours.  
  → **Technical debt**: add idempotency via event deduplication or shift uniqueness.

## Roadmap

- [ ] Idempotency (prevent duplicate processing)
- [ ] Week validation (only Mondays)
- [ ] Timezone support
- [ ] Async processing (Celery + Redis)
  ENDDD