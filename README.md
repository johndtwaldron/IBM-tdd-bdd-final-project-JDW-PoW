# IBM TDD/BDD Final Project — Product Catalog (PoW)

Coursea Course Link ([link](https://www.coursera.org/learn/test-and-behavior-driven-development-tdd-bdd/home/module/1))

Minimal REST service + admin UI for managing Products, built test-first (TDD & BDD).  
Includes unit/integration tests, linting, and end-to-end BDD scenarios that drive the UI via Selenium.

> **Repo:** `johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW`

---

## ✨ Highlights

- **Test-first**: Red → Green → Refactor for models & routes.
- **BDD UI coverage**: `behave` + Selenium scenarios for Create/Read/Update/Delete and filtered search.
- **Clean code checks**: `flake8` + `pylint` wired into `make lint`.
- **Coverage**: `nosetests` with coverage for the `service` package.
- **Dockerized DB**: One-liner to run Postgres for local dev.

---

## 🧱 Tech Stack

- **Python** 3.9+
- **Flask / Gunicorn / Honcho**
- **SQLAlchemy** (+ Postgres)
- **nose / pinocchio** (unit tests)
- **flake8 / pylint** (lint)
- **behave / Selenium** (BDD UI)
- **geckodriver + Firefox** (Selenium driver)

---

## 📁 Project Structure

service/ # Flask app (+ routes, models, common)
features/ # BDD features and step definitions
tests/ # Unit/integration tests + factories
Procfile # Honcho (Procfile-based) process manager
Makefile # Dev shortcuts: lint, tests, run, db
requirements.txt

yaml
Copy code

---

## 🚀 Getting Started

### Prereqs
- Python 3.9+
- Docker (to run Postgres locally)
- Firefox + geckodriver (for `behave` UI tests)
- I ran this in IBM course Lab IDE via browser.

### Setup
```bash
# clone
git clone https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW.git
cd IBM-tdd-bdd-final-project-JDW-PoW
```

# (optional, start a new terminal) create & activate venv
```bash
python3 -m venv venv
source venv/bin/activate
```

# install deps
make install
Start database (Docker)

make db       # starts postgres:alpine on port 5432 with password 'postgres'
Run the service

make run      # honcho start -> serves on http://0.0.0.0:8080
# health check:
curl http://localhost:8080/health
Tip: To stop the service from another shell:

```bash
pkill -f 'gunicorn|honcho' || true
```

---

## 🧪 Testing & Linting
Lint
```bash
make lint     # flake8 (E9/F63/F7/F82 + style) + pylint
```
Unit/Integration + Coverage
```bash
make tests    # nosetests -v tests/test_*.py --with-coverage --cover-package=service
```
BDD (behave + Selenium)
With the service running (make run in one terminal):

```bash
behave
```

Scenarios cover:

Create a Product

Read a Product

Update a Product

Delete a Product

List all Products

Search by Category

Search by Availability

Search by Name

Data seeding for scenarios is handled in features/steps/load_steps.py.

---

## 🌐 REST API
Base: /products

Method	Path	Description
POST	/products	Create a product
GET	/products	List products (supports filters)
GET	/products/<id>	Read one product
PUT	/products/<id>	Update a product
DELETE	/products/<id>	Delete a product

Query Params (list filters)
name=Hat

category=CLOTHS (enum name)

available=true|false|1|0|yes|no

Examples

# list all
```bash
curl -s http://localhost:8080/products
```

# filter by name
```bash
curl -s "http://localhost:8080/products?name=Hat"
```

# filter by category
```bash
curl -s "http://localhost:8080/products?category=CLOTHS"
```

# filter by availability
```bash
curl -s "http://localhost:8080/products?available=true"
```

---

## 🧩 TDD / BDD Approach
TDD (inside-out)
Wrote failing tests for Product model and REST routes, then implemented:

serialization/validation

CRUD methods

query helpers: find_by_name, find_by_category, find_by_availability

endpoints in service/routes.py

BDD (outside-in)
Authored features/products.feature scenarios that drive the actual admin UI with Selenium:

Background data loaded via features/steps/load_steps.py

Reusable web steps in features/steps/web_steps.py (clicking buttons, setting fields, verifying flash messages & results)

---

## 🔗 Quick Links (Files You’ll Cite Later)
These link to the main branch view. 

Fake data / Factories:
tests/factories.py
https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW/blob/main/tests/factories.py

Model Tests (READ/UPDATE/DELETE/LIST/Finders):
tests/test_models.py
https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW/blob/main/tests/test_models.py

Route Tests (CRUD + filters):
tests/test_routes.py
https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW/blob/main/tests/test_routes.py

Routes (CRUD + list filters):
service/routes.py
https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW/blob/main/service/routes.py

BDD Feature (all scenarios):
features/products.feature
https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW/blob/main/features/products.feature

BDD Background Loader:
features/steps/load_steps.py
https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW/blob/main/features/steps/load_steps.py

BDD Web Steps (buttons, messages, results, inputs):
features/steps/web_steps.py
https://github.com/johndtwaldron/IBM-tdd-bdd-final-project-JDW-PoW/blob/main/features/steps/web_steps.py

🛠 Makefile Cheatsheet
```bash
Copy code
make help     # list targets
make install  # pip install -r requirements.txt
make lint     # flake8 + pylint
make tests    # nosetests + coverage
make run      # honcho start
make db       # start Postgres in Docker
make dbrm     # stop & remove Postgres container
```

---

## 🧰 Troubleshooting
Stop server started by Honcho
pkill -f 'gunicorn|honcho' || true

Behave needs the service up
Run make run in one terminal, behave in another.

Postgres not reachable
Ensure make db is running and tests use the right DATABASE_URI.


---


## 📜 License & Credits
Source headers indicate Apache 2.0 (John J. Rofrano).

Built as part of IBM TDD/BDD final project course.


