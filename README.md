# Blackcreek DBMS

A Django-based database management system with PostgreSQL and pgAdmin integration.

**Repository:** [https://github.com/yublueprint/blackcreek_dbms](https://github.com/yublueprint/blackcreek_dbms)

---

## 🚀 Quickstart

<table>
<tr>
<th width="50%">🍎 macOS/Linux</th>
<th width="50%">🪟 Windows</th>
</tr>
<tr>
<td valign="top">

**Clone Repository**
```bash
git clone https://github.com/yublueprint/blackcreek_dbms.git
cd blackcreek_dbms
```

**Setup & Run**
```bash
make build    # Install dependencies
make migrate  # Apply migrations
make run      # Start server
make signup   # Create admin
```

**Clean**
```bash
make clean
```

</td>
<td valign="top">

**Clone Repository**
```bat
git clone https://github.com/yublueprint/blackcreek_dbms.git
cd blackcreek_dbms
```

**Setup & Run**
```bat
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

## 🐘 PostgreSQL + pgAdmin

**Start Services**
```bash
docker compose up -d
```

**Access pgAdmin:** [http://localhost:5050](http://localhost:5050)
- Email: `admin@blackcreek.com`
- Password: `admin`

**Stop Services**
```bash
docker compose down     # Stop
docker compose down -v  # Stop + delete data
```

---

## 🛠️ Troubleshooting

**Check containers:** `docker compose ps`  
**View logs:** `docker compose logs`  
**Restart:** `docker compose restart`

---

## 🔧 Make Commands (macOS/Linux)

| Command | Action |
|---------|--------|
| `make build` | Setup environment |
| `make migrate` | Run migrations |
| `make run` | Start server |
| `make signup` | Create admin |
| `make clean` | Remove venv |