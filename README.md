# Blackcreek DBMS

Django-based database management system with PostgreSQL and pgAdmin.

[![Repository](https://img.shields.io/badge/GitHub-blackcreek__dbms-blue)](https://github.com/yublueprint/blackcreek_dbms)

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Database Setup](#-database-setup)
- [Development Commands](#-development-commands)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🚀 Quick Start

**Prerequisites:** Python 3.8+, Docker, Docker Compose, Git

<table>
<tr>
<th width="50%">🍎 macOS/Linux</th>
<th width="50%">🪟 Windows</th>
</tr>
<tr>
<td valign="top">

```bash
git clone https://github.com/yublueprint/blackcreek_dbms.git
cd blackcreek_dbms

make build
make migrate
make run
make signup  # Create admin
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

## 🐘 Database Setup

```bash
docker compose up -d      # Start
docker compose down       # Stop
docker compose down -v    # Stop + delete data
```

| Service | URL | Credentials |
|---------|-----|-------------|
| Django App | [localhost:8000](http://127.0.0.1:8000) | Via signup |
| pgAdmin | [localhost:5050](http://localhost:5050) | `admin@blackcreek.com` / `admin` |

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

## 🤝 Contributing

```bash
git checkout -b feature/your-feature
git commit -m "Add feature" -m "Description"
git push origin feature/your-feature
# Open pull request
```

---

**Questions?** [Open an issue](https://github.com/yublueprint/blackcreek_dbms/issues) | Part of Yu Blueprint initiative