# Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Client[Client/Browser]
    end
    
    subgraph "Application Layer"
        Django[Django App<br/>Core Service & Producer<br/>Frontend + Backend]
        Analytics[Analytics Engine<br/>Consumer Service]
    end
    
    subgraph "Data Layer"
        Redis[(Redis<br/>Message Queue/Cache)]
        PostgreSQL[(PostgreSQL<br/>Database)]
    end
    
    Client -->|HTTP Requests| Django
    Django -->|Publish Events| Redis
    Django -->|Read/Write| PostgreSQL
    Redis -->|Consume Events| Analytics
    Analytics -->|Read/Write| PostgreSQL
    
    style Django fill:#0c4b33,stroke:#333,stroke-width:2px,color:#fff
    style Analytics fill:#2563eb,stroke:#333,stroke-width:2px,color:#fff
    style Redis fill:#dc2626,stroke:#333,stroke-width:2px,color:#fff
    style PostgreSQL fill:#336791,stroke:#333,stroke-width:2px,color:#fff
    style Client fill:#64748b,stroke:#333,stroke-width:2px,color:#fff
```
    
# Blackcreek DBMS

Django & Spring Boot based database management system with PostgreSQL, Redis.

[![Repository](https://img.shields.io/badge/GitHub-blackcreek__dbms-blue)](https://github.com/yublueprint/blackcreek_dbms)

---

## Table of Contents

- [Quick Start](#-quick-start)
- [Database Setup](#-database-setup)
- [Development Commands](#-development-commands)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## Quick Start

**Prerequisites:** Python 3.8+, Docker, Docker Compose, Git

<table>
<tr>
<th width="50%">macOS/Linux</th>
<th width="50%">Windows</th>
</tr>
<tr>
<td valign="top">

```bash
git clone https://github.com/yublueprint/blackcreek_dbms.git
cd blackcreek_dbms

make build
make migrate
make run
make signup
make test
```

</td>
<td valign="top">

```bat
git clone https://github.com/yublueprint/blackcreek_dbms.git
cd blackcreek_dbms

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
```

</td>
</tr>
</table>

**Access:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Database Setup

```bash
docker compose up -d      # Start
docker compose down       # Stop
docker compose down -v    # Stop + delete data
```

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| Django App | [localhost:8000](http://127.0.0.1:8000) | Via signup | Main application |
| PostgreSQL | localhost:5433 | **user:** `user` <br> **password:** `user` | Primary database |
| pgAdmin | [localhost:5050](http://localhost:5050) | **email:** `admin@blackcreek.com` <br> **password:** `admin` | Database management |
| Redis | localhost:6379 | No authentication | Caching & sessions |
| Redis Commander | [localhost:8081](http://localhost:8081) | No authentication | Redis monitoring |

### Redis Configuration

Redis is used for background tasks.

**Test Redis connection:**
```bash
redis-cli ping
# Should return "PONG"
```

**Trigger analytics manually:**
```bash
redis-cli lpush analytics_events '{ "event": "Hello, Black Creek Farm!" }'
```

---
**Environment Reset:**
- macOS/Linux: `make clean && make build && make migrate`
- Windows: Delete venv folder, recreate with `python -m venv venv`

**Common Issues:**

| Problem | Fix |
|---------|-----|
| Port 8000 in use | Kill process or change port |
| Database error | Check `docker compose ps` |
| Permission denied | Use `sudo` or add user to docker group |

---

## Contributing

```bash
git checkout -b feature/your-feature
git commit -m "Add feature" -m "Description"
git push origin feature/your-feature
# Open pull request
```

---

**Questions?** [Open an issue](https://github.com/yublueprint/blackcreek_dbms/issues) | Part of YU Blueprint initiative
