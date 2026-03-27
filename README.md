# Findly 🔍

A full-stack Django web application for **lost & found item tracking**, featuring real-time messaging, AI-powered matching, QR code scanning, notifications, and a modern responsive UI.

---

## 🚀 Features

- 🔐 **Email-based authentication** with OTP verification
- 📦 **Item Management**: Listing, browsing, search, and claim requests
- 💬 **Real-time Messaging**: WhatsApp-style interface with edit & delete support natively without page reloads
- 🔔 **Live Notifications**: Alerts for messages, claims, and system events
- 📊 **Dashboards**: Comprehensive overview panels with metrics for standard users and administrators
- ⭐ **Reviews & Ratings**: Fostering continuous trust and safety on the platform
- 📷 **QR Code Integration**: Generation and scanning for items and profiles
- 🤖 **AI-powered Engine**: Smart suggestions and computational views
- 🌗 **UI & Accessibility**: Modern "TheyMakeDesign" soft, airy aesthetic with Dark mode / Light mode support

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0.2, Django REST Framework |
| **Database** | PostgreSQL (local) / Render PostgreSQL (production) |
| **Storage** | WhiteNoise (static) + Django MEDIA (uploads) |
| **Auth** | Custom User model (email-based) |
| **Email** | Gmail SMTP via App Password |
| **Deployment** | Render + Gunicorn |
| **Frontend** | Tailwind CSS (via CDN), Bootstrap Icons, Inter Font |

---

## 📁 Core Application Architecture

The project is organized into modular Django apps to separate concerns efficiently:

- **`accounts/`**: Handles all user authentication models and views. Uses a custom User model (email as primary identifier).
- **`items/`**: The core application. Users can browse items, search for specific listings, list their own items, and submit claim requests.
- **`messaging/`**: A robust chat engine enabling direct user-to-user communication. Features speech bubbles, async editing, and native deletion.
- **`notifications/`**: A centralized alerting system delivering dynamically rendered notification cards.
- **`dashboard/`**: Provides comprehensive overview panels indicating recent activity for both users and admins.
- **`reviews/`**: Allows users to leave feedback, ratings, and comments.
- **`qr/`**: Integrates QR code generation and scanning directly into the application.
- **`ai/`**: A dedicated application for AI-powered features and deep integrations.
- **`core/`**: Contains the foundational templates, fallback views, and standard site logic.

---

## 🎨 UI / UX Design Principles

- Uses a unified **"TheyMakeDesign"** soft, airy aesthetic.
- **Tailwind CSS** is the primary styling engine, leveraging utility-first classes.
- **Dark Mode and Light Mode** are fully supported locally via local storage and system preference detection.
- **Dynamic JavaScript features** (like Edit/Delete modals) utilize asynchronous JSON Fetch API requests without complex dependencies.

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
pip install -r requirements.txt
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
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

> ✅ If using `venv`, make sure it's activated, or run `..\venv\Scripts\python manage.py <command>`.

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
