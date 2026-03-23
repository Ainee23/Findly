# Findly 🔍

A full-stack Django web application for **lost & found item tracking**, featuring real-time messaging, AI-powered matching, QR code scanning, notifications, and a modern responsive UI.

---

## 🚀 Features

- 🔐 Email-based authentication with OTP verification
- 📦 Item listing, browsing, search, and claim requests
- 💬 Real-time WhatsApp-style messaging (edit & delete support)
- 🔔 Live notifications (messages, claims, system alerts)
- 📊 User & admin dashboards with activity metrics
- ⭐ User reviews and ratings system
- 📷 QR code generation and scanning for items/profiles
- 🤖 AI-powered item matching
- 🌗 Dark mode / Light mode support

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0.2, Django REST Framework |
| Database | PostgreSQL (local) / Render PostgreSQL (production) |
| Storage | WhiteNoise (static) + Django MEDIA (uploads) |
| Auth | Custom User model (email-based) |
| Email | Gmail SMTP via App Password |
| Deployment | Render + Gunicorn |
| Frontend | Vanilla CSS, Bootstrap Icons, Inter Font |

---

## ⚙️ Local Setup

### 1. Clone and create virtual environment
```bash
git clone <your-repo-url>
cd Findly
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r Findly/requirements.txt
```

### 3. Create `.env` file inside `Findly/` (next to `manage.py`)
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_16_digit_app_password

DB_PASSWORD=your_postgres_password

# On Render only:
# DATABASE_URL=postgres://user:pass@host/dbname
```

### 4. Apply migrations and run
```bash
cd Findly
..\venv\Scripts\python manage.py migrate
..\venv\Scripts\python manage.py runserver
```

> ✅ Always use `..\venv\Scripts\python` to ensure the venv Python is used, not the system Python.

---

## 📧 Gmail SMTP Setup

To send real verification emails:
1. Enable **2-Step Verification** on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an App Password (16 characters)
4. Set it as `EMAIL_HOST_PASSWORD` in your `.env`

---

## ☁️ Render Deployment

### Environment Variables to set in Render:
| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Your Django secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `findly.onrender.com` |
| `EMAIL_HOST_USER` | Your Gmail address |
| `EMAIL_HOST_PASSWORD` | Gmail App Password |
| `DATABASE_URL` | Render PostgreSQL URL |

### Build & Start Commands:
```bash
# Build command:
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate

# Start command:
gunicorn Findly.wsgi:application
```

---

## 📁 Project Structure

```
Findly/
├── Findly/           # Django project (settings, urls, wsgi)
├── core/             # Custom User model, middleware, home views
├── accounts/         # Auth: login, register, OTP verify, profile
├── items/            # Item listing, search, claims
├── messaging/        # Direct messaging (edit/delete)
├── notifications/    # Alerts and notification feed
├── dashboard/        # User & admin dashboards
├── reviews/          # Ratings and reviews
├── qr/               # QR code generation/scanning
├── ai/               # AI matching engine
├── templates/        # All HTML templates
├── static/           # CSS, JS, images
├── media/            # User-uploaded files (gitignored)
├── requirements.txt
└── .env              # ← Never commit this!
```

---

## 📋 Pre-Deploy Checklist

- [ ] Login & register working
- [ ] Email verification working
- [ ] Image uploads working (profile, item, QR)
- [ ] Chat (send, edit, delete) working
- [ ] Notifications working
- [ ] Dashboard loading correctly
- [ ] Admin panel accessible
- [ ] PostgreSQL connected
- [ ] `DEBUG=False` on production
- [ ] `.env` added to `.gitignore` ✅

---

## 👩‍💻 Author

**Ainee Makwana** — Final Year Project, 2026
