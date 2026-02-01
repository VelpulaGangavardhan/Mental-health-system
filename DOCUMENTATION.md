# 🧠 Advanced Mental Health Platform - Complete Documentation

## Project Overview

Your Flask-based Mental Health Platform has been transformed into an **enterprise-grade application** with comprehensive mental health assessment, tracking, analytics, and user management capabilities.

---

## 📊 What's New - Advanced Features

### **1. User Management System** 👥
- Email-based registration and login
- User profile management with bio
- Secure password change functionality
- Role-based access control (User/Admin)
- Account timestamps and metadata

**Files Modified**: `models.py`, `forms.py`, `app.py`
**Templates**: `profile.html`, `edit_profile.html`, `change_password.html`

---

### **2. Extended Assessment System** 📋
Comprehensive 10-question assessment covering:
- **Stress Assessment** (2Q)
- **Anxiety Assessment** (2Q)
- **Sleep Quality** (2Q)
- **Depression Indicators** (2Q)
- **Social Support** (2Q)

**Route**: `/extended-screening`
**Template**: `extended_screening.html`, `extended_result.html`

---

### **3. Screening History & Visualization** 📈
- Complete assessment history with timestamps
- Interactive Chart.js visualizations
- Trend detection (Improving/Worsening/Stable)
- Sortable and filterable results
- Visual score progression tracking

**Route**: `/history`
**Template**: `screening_history.html`

---

### **4. Analytics Dashboard** 📊
- Statistical summary (total, average, range)
- Risk level distribution charts
- Trend analysis with insights
- Performance metrics
- Intelligent recommendations

**Route**: `/analytics`
**Template**: `analytics.html`

---

### **5. Coping Strategy Tracker** 🛠️
- Log personal coping strategies
- Effectiveness rating system (1-5)
- Strategy descriptions and notes
- Historical tracking and review
- Personal strategy library

**Routes**: `/coping-strategies`, `/log-strategy`
**Templates**: `coping_strategies.html`, `log_strategy.html`

---

### **6. Data Export & Management** 💾
- CSV export of all screening data
- Includes all component scores
- Date-stamped export files
- Compatible with Excel/Data Analysis tools

**Route**: `/export-data`

---

### **7. Admin Dashboard** 🔐
- System-wide statistics
- Complete user management
- Role assignment and revocation
- User account deletion
- Admin self-protection

**Route**: `/admin`
**Template**: `admin_dashboard.html`

---

### **8. Enhanced Dashboard** 🏠
- Personalized welcome message
- Key metrics overview
- Recent screenings table
- Quick action buttons
- Account statistics

**Route**: `/dashboard`
**Template**: `dashboard.html` (Enhanced)

---

### **9. Intelligent Recommendations** 💡
- Dynamic recommendation generation
- Risk-level based suggestions
- Professional support resources
- Coping technique recommendations
- Crisis hotline information

---

### **10. Improved Navigation** 🧭
- Dropdown Tools menu
- Context-aware navigation
- Mobile-responsive design
- Admin panel link for admins
- Quick access buttons

**Modified**: `base.html`

---

## 🗂️ Project Structure

```
New folder (2)/
├── app.py                          # Main Flask application
├── models.py                       # Database models (enhanced)
├── forms.py                        # WTForms (enhanced)
├── requirements.txt                # Dependencies (updated)
├── database.db                     # SQLite database
├── FEATURES_ADDED.md              # Complete feature list
├── QUICKSTART.md                   # User guide
├── README.md                       # Original readme
├── static/
│   └── style.css                  # Styling
├── templates/
│   ├── base.html                  # Navigation (enhanced)
│   ├── dashboard.html             # Dashboard (new)
│   ├── profile.html               # User profile (NEW)
│   ├── edit_profile.html          # Edit profile (NEW)
│   ├── change_password.html       # Password change (NEW)
│   ├── extended_screening.html    # Extended assessment (NEW)
│   ├── extended_result.html       # Assessment results (NEW)
│   ├── screening_history.html     # History view (NEW)
│   ├── analytics.html             # Analytics (NEW)
│   ├── coping_strategies.html     # Strategies list (NEW)
│   ├── log_strategy.html          # Log strategy (NEW)
│   ├── admin_dashboard.html       # Admin panel (NEW)
│   ├── screening.html             # Quick screening
│   ├── result.html                # Quick result
│   ├── login.html                 # Login page
│   ├── register.html              # Registration
│   ├── index.html                 # Homepage
│   ├── awareness.html             # Awareness info
│   └── support.html               # Support resources
├── instance/                      # Instance folder
└── tests/                         # Test files
```

---

## 🗄️ Database Schema

### **User Model**
```python
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (Hashed)
- role ('user' or 'admin')
- created_at (Timestamp)
- updated_at (Timestamp)
- bio (Text)
- preferences (JSON)
```

### **Screening Model**
```python
- id (Primary Key)
- user_id (Foreign Key)
- score (Integer)
- level ('Low', 'Moderate', 'High')
- created_at (Timestamp)
- notes (Text)
- stress_score
- anxiety_score
- sleep_score
- depression_score
- social_score
```

### **CopingLog Model** (NEW)
```python
- id (Primary Key)
- user_id (Foreign Key)
- strategy (String)
- description (Text)
- effectiveness (1-5 Rating)
- created_at (Timestamp)
```

### **Recommendation Model** (NEW)
```python
- id (Primary Key)
- screening_id (Foreign Key)
- category ('professional', 'coping', 'resource')
- title (String)
- description (Text)
- url (Optional Link)
```

---

## 🔐 Security Features

✅ **Password Security**: Werkzeug password hashing
✅ **Authorization**: Admin-required decorator for admin routes
✅ **Authentication**: Flask-Login session management
✅ **CSRF Protection**: Flask-WTF token validation
✅ **Input Validation**: WTForms validation on all inputs
✅ **Data Protection**: Database cascade delete for cleanup
✅ **Admin Safety**: Self-deletion prevention

---

## 📡 API Routes

### **Authentication**
| Route | Method | Description |
|-------|--------|-------------|
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |

### **Core Features**
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage |
| `/dashboard` | GET | User dashboard |
| `/screening` | GET, POST | Quick screening |
| `/extended-screening` | GET, POST | Extended assessment |
| `/awareness` | GET | Awareness information |
| `/support` | GET | Support resources |

### **User Management**
| Route | Method | Description |
|-------|--------|-------------|
| `/profile` | GET | View profile |
| `/profile/edit` | GET, POST | Edit profile |
| `/change-password` | GET, POST | Change password |

### **Data & Analytics**
| Route | Method | Description |
|-------|--------|-------------|
| `/history` | GET | Screening history |
| `/analytics` | GET | Analytics dashboard |
| `/export-data` | GET | Download CSV |

### **Coping Strategies**
| Route | Method | Description |
|-------|--------|-------------|
| `/coping-strategies` | GET | View strategies |
| `/log-strategy` | GET, POST | Log new strategy |

### **Admin Features**
| Route | Method | Description |
|-------|--------|-------------|
| `/admin` | GET | Admin dashboard |
| `/admin/users/<id>/toggle-admin` | POST | Toggle admin role |
| `/admin/users/<id>/delete` | POST | Delete user |

---

## 🎨 UI Components

### **Cards & Displays**
- Metric cards with icons
- Assessment result cards
- User profile cards
- Strategy cards with ratings
- Alert cards for insights

### **Charts & Visualizations**
- Line chart for score trends (Chart.js)
- Doughnut chart for risk distribution
- Responsive design for mobile
- Interactive elements

### **Forms**
- Registration form (email support)
- Extended screening form (10 fields)
- Profile edit form
- Password change form
- Strategy logging form

### **Tables**
- Screening history table
- User management table
- Strategy list table

---

## 🚀 Getting Started

### **Installation**
```bash
cd "New folder (2)"
pip install -r requirements.txt
python app.py
```

### **Access the App**
- Open browser: `http://localhost:5000`
- Register new account or login
- Start with Quick Screening or Extended Assessment

### **Create Admin User**
In Python shell:
```python
from app import app
from models import User, SessionLocal

with app.app_context():
    session = SessionLocal()
    user = User(username='admin', email='admin@example.com', role='admin')
    user.set_password('password123')
    session.add(user)
    session.commit()
```

---

## 📚 Key Technologies

- **Backend**: Flask 2.2+
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Frontend**: Bootstrap 5.3
- **Charts**: Chart.js
- **Security**: Werkzeug password hashing

---

## 📝 Forms Reference

### **RegisterForm**
- username (required, 3-120 chars)
- email (optional, valid email)
- password (required, min 6 chars)
- confirm_password (must match)

### **ProfileForm**
- username (required, 3-120 chars)
- email (optional, valid email)
- bio (optional, max 500 chars)

### **ChangePasswordForm**
- current_password (required)
- new_password (required, min 6)
- confirm_password (must match)

### **ExtendedScreeningForm**
- 10 radio button questions
- Optional notes (max 500 chars)

### **CopingLogForm**
- strategy (required, 3-255 chars)
- description (optional, max 500 chars)
- effectiveness (1-5 rating, optional)

---

## 🎯 Features by User Type

### **Regular Users**
- ✅ Register/Login with email
- ✅ Take quick and extended assessments
- ✅ View screening history
- ✅ See analytics and trends
- ✅ Log coping strategies
- ✅ Export personal data
- ✅ Manage profile and password
- ✅ Get personalized recommendations

### **Admin Users**
- ✅ All regular user features
- ✅ Access admin dashboard
- ✅ View all users
- ✅ Manage user roles
- ✅ Delete user accounts
- ✅ View system statistics

---

## 💡 Use Cases

### **Mental Health Monitoring**
Track your mental health over time with weekly assessments and visual trends.

### **Treatment Support**
Share screening results with healthcare providers for better care.

### **Coping Strategy Development**
Build a personal library of effective coping strategies with ratings.

### **Data Analysis**
Export data for personal analysis or research purposes.

### **Professional Administration**
Manage users and monitor system usage (admin only).

---

## 📊 Sample Workflow

1. **Register** → Create account with email
2. **First Assessment** → Take extended screening
3. **View Results** → See score breakdown and recommendations
4. **Log Strategies** → Add coping techniques that helped
5. **Monitor Progress** → Check history and analytics
6. **Share Data** → Export results for doctor
7. **Update Profile** → Keep information current

---

## 🔧 Customization Options

### **Modify Assessment Questions**
Edit `/extended-screening` form in `forms.py`

### **Change Scoring Algorithm**
Update score calculation in `get_recommendations()` function

### **Add New Features**
Extend models, create forms, add routes and templates

### **Customize Styling**
Edit `static/style.css` and template HTML

---

## 📄 Documentation Files

1. **FEATURES_ADDED.md** - Detailed feature documentation
2. **QUICKSTART.md** - User guide and tips
3. **README.md** - Original project readme
4. **This file** - Complete technical reference

---

## 🐛 Troubleshooting

**Issue**: Database errors
- **Solution**: Delete `database.db` and restart

**Issue**: Import errors
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Can't login
- **Solution**: Check username/email spelling, use registration if needed

**Issue**: Admin routes not accessible
- **Solution**: Change user role to admin via database or code

---

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Bootstrap 5: https://getbootstrap.com/docs/5.3/
- Chart.js: https://www.chartjs.org/

---

## 📞 Support

For issues or questions:
1. Check QUICKSTART.md for user guide
2. Review FEATURES_ADDED.md for feature details
3. Examine template files for UI reference
4. Check models.py for database schema

---

## ✅ Checklist for Deployment

- [ ] Update SECRET_KEY in production
- [ ] Set DATABASE_URL for production database
- [ ] Create admin account
- [ ] Test all features
- [ ] Configure email (optional)
- [ ] Set up HTTPS
- [ ] Configure CORS if needed
- [ ] Set DEBUG=False in production

---

**Version**: 2.0 Advanced Edition
**Status**: Production Ready
**Last Updated**: February 2026

---

Enjoy your advanced mental health platform! 🎉
