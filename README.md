# Findly 🔍

> **A smart Lost & Found platform** — connecting people who've lost items with those who've found them, powered by AI matching, QR codes, and real-time location sharing.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-findly--4usu.onrender.com-6C63FF?style=for-the-badge)](https://findly-4usu.onrender.com)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Smart Matching** | Multi-factor similarity scoring (text + image + location) using TF-IDF and perceptual hashing |
| 📷 **QR Code System** | Generate & scan QR codes for items and user profiles |
| 📍 **Live Location Sharing** | Real-time GPS tracking between claimant and owner during pickup |
| 🔐 **OTP Email Verification** | Secure account registration with Gmail SMTP OTP |
| 💬 **Messaging System** | In-app direct messaging between users |
| 📊 **Admin Dashboard** | Platform-wide stats, item management, and user oversight |
| 🌙 **Dark Mode** | Full light/dark theme toggle with persistent preference |
| ☁️ **Cloud Media Storage** | Cloudinary CDN for persistent image uploads |
| 🗺️ **Map View** | Interactive map showing all item locations |
| ⭐ **Review System** | Leave reviews for owners and finders after item return |

---

## 🛠️ Tech Stack

- **Backend:** Django 6.0, Django REST Framework
- **Database:** PostgreSQL (local) / Render PostgreSQL (production)
- **Frontend:** HTML, Bootstrap 5, Tailwind CSS, Vanilla JS
- **AI Matching:** ImageHash (perceptual hashing), difflib (text similarity)
- **Media Storage:** Cloudinary CDN
- **Static Files:** WhiteNoise
- **Deployment:** Render (Web Service + PostgreSQL)
- **Email:** Gmail SMTP (OTP verification)

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/findly.git
cd findly
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_PASSWORD=your-postgres-password

# Email (Gmail SMTP)
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cloudinary (optional for local dev)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 3. Run Migrations & Start
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🌐 Deployment (Render)

### Required Environment Variables on Render

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | Auto-set by Render PostgreSQL |
| `EMAIL_HOST_USER` | Gmail address for OTP emails |
| `EMAIL_HOST_PASSWORD` | Gmail App Password |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary dashboard → Cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary dashboard → API Key |
| `CLOUDINARY_API_SECRET` | Cloudinary dashboard → API Secret |

### Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command
```bash
gunicorn Findly.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 📁 Project Structure

```
Findly/
├── accounts/        # User auth, OTP, profiles
├── ai/              # Smart matching engine (text + image similarity)
├── core/            # Custom User model, middleware, home views
├── dashboard/       # Admin & user dashboards
├── items/           # Item CRUD, claims lifecycle, map
├── messaging/       # Direct messaging between users
├── notifications/   # In-app notification system
├── qr/              # QR code generation & scanning
├── reviews/         # Star ratings & reviews
├── templates/       # All HTML templates
├── static/          # CSS, JS, images
└── media/           # Local uploads (replaced by Cloudinary in production)
```

---

## 🔄 Claim Lifecycle

```
User finds item → Submits claim (with proof) → Owner reviews
      ↓                                              ↓
Owner requests more proof          Owner approves (or rejects)
                                          ↓
                              Claimant shares live GPS location
                                          ↓
                              Claimant clicks "Confirm Pickup"
                                          ↓
                              Both users leave reviews ⭐
```

---

## 📄 License

This project was built as a college project. Feel free to use it as inspiration.

---

*Built with ❤️ using Django + Bootstrap + Cloudinary*
