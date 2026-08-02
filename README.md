# Anuj Biswal — AI/ML Engineer Portfolio

A production-ready personal portfolio with a **dark glassmorphism viewer site** and a **modern admin dashboard**, built with Django + Bootstrap 5 + vanilla JavaScript (ES6+).

---

## ✨ Features

### Viewer Website
- Full-screen animated hero (particles, typing roles, gradient blobs, glassmorphism)
- Pages: Home, About, Projects, Certificates, Achievements, Skills, Resume, Contact, Gallery, Experience, Timeline
- Project cards with live demo / GitHub links, tech chips, status + featured badges, search, filters, pagination
- Certificate cards with image/PDF preview, verify links, filter + search
- Skills with animated linear & circular progress, grouped by category
- Floating **AI Assistant** (bottom-right) that answers predefined portfolio FAQs — no LLM, no API, instant
- Contact form with honeypot anti-spam, stored in the database
- Lightbox gallery, lazy loading, scroll-reveal animations, custom scrollbar, back-to-top, theme toggle (dark/light)
- Fully responsive, accessible, SEO meta tags

### Admin Dashboard (`/admin-panel/`)
- Glassmorphism dark login page (animated background)
- Statistics cards (projects, certificates, skills, messages) + Chart.js charts
- Manage everything: Profile, About, Skills, Projects, Certificates, Achievements, Gallery, Resume, Experience, Education, Social Links, Messages, FAQ AI, Settings
- Generic CRUD engine — one view powers every resource (list/add/edit/delete)
- Read / delete / mark-read contact messages with search
- POST-only deletions (CSRF-safe)

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django 5.x |
| Frontend | HTML5, CSS3, Bootstrap 5, Bootstrap Icons, Vanilla JS (ES6+) |
| Database | SQLite (dev) → PostgreSQL (prod, easy switch) |
| Static files | WhiteNoise (production) |
| Charts | Chart.js (CDN) |

---

## 📁 Folder Structure

```
anuj-portfolio/
├── portfolio/               # Project config (settings, urls, wsgi, asgi)
├── apps/
│   └── core/                # The single Django app
│       ├── models.py        # Normalized data models
│       ├── forms.py         # ModelForms + contact form (honeypot)
│       ├── views.py         # Public viewer views
│       ├── admin_views.py   # Admin panel views (dashboard, CRUD, messages)
│       ├── middleware.py    # Visitor tracking
│       ├── context_processors.py  # site-wide globals
│       ├── templatetags/    # Custom template tags/filters
│       └── management/commands/seed_data.py
├── templates/               # viewer/, admin/, partials/ — reusable templates
├── static/                  # css/, js/, img/
├── media/                   # Uploaded images / PDFs (gitignored)
├── requirements.txt
├── .env.example             # Copy to .env and fill in
└── README.md
```

---

## 🚀 Quick Start (Local)

```bash
# 1. Create & activate a virtual environment
python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env        # edit values as needed

# 4. Migrate, seed, and run
python manage.py migrate
python manage.py seed_data   # creates admin + demo content
python manage.py runserver
```

Open **http://127.0.0.1:8000/** for the site and **http://127.0.0.1:8000/admin-panel/** for the dashboard.

### Default admin credentials (from seed)

> Username: `Anuj-2006` · Password: `Anuj@2006`

Change the password immediately after first login (`admin-panel` → Settings, or Django shell). The password is **not** hard-coded — it is read from `ADMIN_PASSWORD` in your `.env`. The app also syncs the admin account from `ADMIN_USERNAME` / `ADMIN_PASSWORD` on every startup (see `apps/core/startup.py`), so every deploy gets a working admin login.

---

## 🌍 Deployment

### Option A — Render / Railway / PythonAnywhere (Django)
1. Set environment variables: `DJANGO_SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=yourdomain.com`, `CSRF_TRUSTED_ORIGINS=https://yourdomain.com`
2. Run `python manage.py migrate` then `python manage.py seed_data` on the host
3. Collect static: `python manage.py collectstatic --noinput` (WhiteNoise serves them)
4. Upload media files (resume PDFs, images) through the admin panel

### Option B — Vercel (frontend)
- The viewer is server-rendered by Django, so it ships as one app. For a split setup, export the templates/static to a static host and proxy API calls — but the simplest production topology is a single Python host above.

### Production checklist
- `DEBUG=False`, strong `DJANGO_SECRET_KEY` in `.env`
- `ALLOWED_HOSTS` + `CSRF_TRUSTED_ORIGINS` set
- HTTPS enabled at the host level
- Run `python manage.py collectstatic --noinput` after deploy

---

## 🔐 Security

- CSRF protection on all forms; deletes are POST-only
- `login_required`-style `admin_required` decorator on every admin view
- Honeypot anti-spam on the contact form
- No hardcoded secrets — everything comes from environment variables
- Secure file uploads (Django validated ImageField/FileField)
- Auto-escaping in templates; AI assistant renders with `textContent` (no XSS)

---

## 🧠 AI Assistant (FAQ-only)

The floating assistant is **not** a chatbot. It serves predefined Q&A stored in the `FAQ` model, managed from the admin panel. Out-of-scope questions get: *"I'm designed to answer only portfolio-related questions."* No LLM, no API, no external service — fast and lightweight.

---

## 🔮 Future Improvements

- PostgreSQL switch (change `DATABASES` in settings; Django supports both)
- Cache FAQ API with Django's cache framework
- Rate-limit the contact form and admin login
- Add analytics (the `Visitor` model already tracks visits)
- Email notifications for new contact messages
- i18n support

---

## 📄 License

Personal portfolio project — free to use and extend.
