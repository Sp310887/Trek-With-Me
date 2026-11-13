# ⛰️ Trek With Me
### "Push Your Limits" — A Full-Stack Trekking Web Application

---

## 🚀 Quick Setup Guide

### 1. Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database
1. Open MySQL Workbench or terminal
2. Run the database script:
```sql
source database.sql
```
Or copy-paste the contents of `database.sql` into MySQL.

### 4. Configure Database Connection
Open `app.py` and update the DB_CONFIG section:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'trek_with_me',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD'  # ← Change this
}
```

### 5. Run the Application
```bash
python app.py
```
Open your browser at: **http://localhost:5000**

> Note: This project is a Flask app, not a Streamlit app. Do not use `streamlit run app.py`.

---

## 👤 Demo Credentials

| Role  | Email                    | Password  |
|-------|--------------------------|-----------|
| User  | (use your own account)   | (your password) |

---

## 📁 Project Structure

```
trek_with_me/
├── app.py               # Flask backend (all routes)
├── database.sql         # MySQL schema + seed data
├── requirements.txt     # Python dependencies
├── README.md
└── templates/
    ├── base.html        # Base layout + navbar + footer
    ├── index.html       # Home page with hero + featured treks
    ├── treks.html       # Trek listing with filters + distance
    ├── trek_detail.html # Single trek detail page
    ├── register.html    # User registration
    ├── login.html       # User login
    ├── booking.html     # Trek booking form
    ├── payment.html     # UPI payment (demo)
    ├── my_bookings.html # User booking history
    ├── sos.html         # SOS emergency page
    ├── contact.html     # Contact form
    └── admin.html       # Admin dashboard
```

---

## ✨ Features

| Module             | Description                                              |
|--------------------|----------------------------------------------------------|
| 🏠 Home            | Hero with parallax, featured treks, smart recommendations|
| 🗺️ Trek Listing    | Filter by difficulty, search, GPS distance display       |
| 📋 Trek Detail     | Full info, homestay options, distance calculator         |
| 👤 Auth            | Register, Login, Logout with session management          |
| 📅 Booking         | Date, people, homestay selection with price calculator   |
| 💳 Payment         | Demo UPI QR code payment with countdown timer            |
| 🆘 SOS             | GPS location SOS alert, emergency contacts               |
| 📞 Contact         | Contact form with message storage                        |
| 🔐 Admin           | Full dashboard: treks, bookings, users, messages, SOS    |
| 🧠 Recommendations | Smart API endpoint filtering by difficulty + budget      |

---

## 🛠️ Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python + Flask
- **Database**: MySQL
- **APIs**: Geolocation API (distance calculation)
- **Fonts**: Bebas Neue, Montserrat, Playfair Display
- **Icons**: Font Awesome 6

---

## 🎨 Design Theme
- **Color Palette**: Forest greens, mountain gold, night sky dark
- **Typography**: Bebas Neue (display), Montserrat (body)
- **Style**: Dark adventurous aesthetic with parallax backgrounds

---

*Made with ❤️ for adventurers · Trek With Me © 2024*
