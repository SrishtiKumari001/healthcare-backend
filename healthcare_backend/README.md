# Vitals — Healthcare Backend

A production-style backend for a healthcare application, built with **Django**, **Django REST Framework**, **PostgreSQL**, and **JWT authentication** — plus a polished, dark "clinical command-center" dashboard so the API isn't just something you test in Postman, it's something you can actually *look at*.

![status](https://img.shields.io/badge/status-ready-34E4B4) ![python](https://img.shields.io/badge/python-3.10+-blue) ![django](https://img.shields.io/badge/django-5.0-092E20)

---

## ✨ What's inside

- **JWT authentication** (`djangorestframework-simplejwt`) — register, login, token refresh
- **Patients API** — full CRUD, scoped to the logged-in user who created each record
- **Doctors API** — full CRUD, visible to every authenticated user
- **Patient ↔ Doctor mapping API** — assign / unassign doctors, look up all doctors for one patient
- **PostgreSQL** as the datastore, all config driven by environment variables (`.env`)
- **Consistent error handling** — every response follows `{ success, message, data|errors }`
- **Input validation** on every field (phone numbers, age ranges, duplicate emails, duplicate assignments…)
- **Swagger / OpenAPI docs** auto-generated at `/api/docs/`
- **A full dashboard UI** (`/`) — login/register screen, live stats, patient & doctor tables with add/edit/delete modals, and an assignment manager. Talks to the API with plain JS + `fetch`, no build step required.

---

## 🗂 Project structure

```
healthcare_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── healthcare_backend/       # project settings, urls, custom exception handler
├── accounts/                 # custom User model + register/login/refresh
├── patients/                 # Patient model, serializer, viewset
├── doctors/                  # Doctor model, serializer, viewset
├── mappings/                 # PatientDoctorMapping model, serializer, viewset
├── templates/index.html      # the dashboard UI
└── static/                   # (reserved for extra static assets)
```

---

## 🚀 Getting started

### 1. Clone & create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up PostgreSQL
Create a database and user (adjust names as you like):
```sql
CREATE DATABASE healthcare_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO postgres;
```

### 3. Configure environment variables
```bash
cp .env.example .env
# then edit .env with your real SECRET_KEY and DB credentials
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. (Optional) Create an admin superuser
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

Now open:
- **Dashboard:** http://127.0.0.1:8000/
- **Swagger API docs:** http://127.0.0.1:8000/api/docs/
- **Django admin:** http://127.0.0.1:8000/admin/

---

## 🔑 API endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register with `name`, `email`, `password` |
| POST | `/api/auth/login/` | Log in with `email`, `password` → returns JWT tokens |
| POST | `/api/auth/refresh/` | Exchange a refresh token for a new access token |
| GET | `/api/auth/me/` | Current user's profile (auth required) |

### Patients (auth required)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Add a new patient |
| GET | `/api/patients/` | List patients **you created** |
| GET | `/api/patients/<id>/` | Patient details |
| PUT | `/api/patients/<id>/` | Update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |

### Doctors (auth required)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Add a new doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Doctor details |
| PUT | `/api/doctors/<id>/` | Update a doctor |
| DELETE | `/api/doctors/<id>/` | Delete a doctor |

### Patient–Doctor mappings (auth required)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List your assignments |
| GET | `/api/mappings/<patient_id>/` | All doctors assigned to a patient |
| DELETE | `/api/mappings/<id>/` | Remove an assignment |

All authenticated requests need:
```
Authorization: Bearer <access_token>
```

---

## 🧪 Quick test with curl

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Dr. Asha Verma","email":"asha@example.com","password":"StrongPass123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"asha@example.com","password":"StrongPass123"}'

# Add a patient (replace <TOKEN>)
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"name":"Ravi Kumar","age":34,"gender":"male","contact_number":"9876543210"}'
```

---

## 🎨 About the dashboard

The UI lives entirely in `templates/index.html` (served by Django at `/`) — a single self-contained file with a "clinical command-center" look: deep navy background, a mint vital-signs accent, and one signature animated ECG line on the login screen. It talks to the same API described above using the browser's `fetch`, stores JWTs in `localStorage`, and auto-refreshes expired access tokens. No frontend build tooling needed — just run the Django server and open the page.

---

## 🧱 Notes on design choices

- **Patients are private to their creator** — the spec asked for `GET /api/patients/` to return only patients the logged-in user created, so patient detail/update/delete are also scoped to the owner (a user can't edit someone else's patient by guessing an ID).
- **Doctors are shared** — any authenticated user can see the full doctor roster, matching the spec's plain "retrieve all doctors."
- **Duplicate assignments are blocked** at the database level (`unique_together` on patient + doctor) and validated in the serializer with a friendly error message.
- **Error handler** in `healthcare_backend/exceptions.py` normalizes every DRF error into `{ success: false, message, errors }` so the frontend (or any client) never has to special-case error shapes.

Good luck — and enjoy showing this one off. 🚀
