```mermaid
graph LR
    A[Client] -->|HTTP/JSON| B[Django API\n(sync, DRF)]
    B -->|Read/Write| C[(PostgreSQL)]
    B -->|PUBLISH event| D[(Redis Streams)]
    D -->|CONSUME event| E[Async Worker\n(aggregation logic)]
    E -->|Update aggregates| C
```


### Domain Model (TDD)

```mermaid
graph TD
    A[Client] -->|HTTP| B[Django API]
    B --> C[wfm_core.Shift]
    C --> D[(PostgreSQL)]
    C -->|event| E[Redis]
    E --> F[Async Worker]
    F --> G[wfm_core.WeeklyWorkload]

    style C fill:#d4f7e5,stroke:#2e8b57
```