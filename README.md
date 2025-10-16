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

### 7. Create an Admin/SuperUser

```bat
python manage.py createsuperuser
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

**Admin Panel:** [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)


## End-to-End (E2E) Testing Setup

This project uses **pytest** and **Playwright** for E2E browser testing.

### 1. Install Testing Dependencies

First, activate your virtual environment:

```bat
venv\Scripts\activate
```

Then install the testing dependencies:

```bat
pip install -r requirements-test.txt
python -m playwright install
```

### 2. Test User Setup

A test admin user will be created automatically by the test fixtures with these credentials:

- **Username:** `testadmin`
- **Password:** `testpass123`
- **Email:** `admin@blackcreek.com`

### 3. Running the Tests

Start your Django development server in one terminal:

```bat
python manage.py runserver
```

In another terminal, run the E2E tests:

```bat
pytest tests/e2e/ -v
```

To see the browser window during tests (for debugging):

```bat
pytest tests/e2e/ -v --headed
```
