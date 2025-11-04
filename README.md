# Blackcreek DBMS

A Django-based database management system for managing and tracking records.

Repository: [https://github.com/yublueprint/blackcreek_dbms](https://github.com/yublueprint/blackcreek_dbms)

---

## Quickstart (MAC)

### 1. Clone the Repository from desktop

```bash
git clone https://github.com/yublueprint/blackcreek_dbms.git
cd blackcreek_dbms
```

### 2. Build the Project

```bash
make build
```

- Creates a virtual environment (`venv`)
- Installs dependencies from `requirements.txt`

### 3. Migrate

```bash
make migrate
```

### 4. Run the Development Server

```bash
make run
```

### 5. Create an Admin/SignUp

```bash
make signup
```

### 6. Clean the Venv

```bash
make clean
```

### Local Development Server

**[Open the app at http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## Quickstart (Windows)

### 1. Clone the Repository

```bat
git clone https://github.com/yublueprint/blackcreek_dbms.git
cd blackcreek_dbms
```

### 2. Create a Virtual Environment

```bat
python -m venv venv
```

### 3. Activate the Virtual Environment

```bat
venv\Scripts\activate
```

### 4. Install Dependencies

```bat
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```bat
python manage.py migrate
```

### 6. Run the Development Server

```bat
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)


```bash
docker build -t blackcreek-dbms:latest .
docker run -p 8000:8000 blackcreek-dbms:latest
