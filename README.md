# 🧠 Mental Health Platform - Advanced Edition v2.0

## 📊 Project Overview

This is a **professional-grade Flask application** for mental health screening and wellness tracking. It provides comprehensive assessment tools, progress tracking, analytics, and admin features.

### ✨ **Major Features Added in v2.0**

- ✅ **Email-based User Management** - Registration, profiles, password management
- ✅ **Extended Assessments** - 10-question comprehensive mental health evaluation
- ✅ **Screening History** - Track assessments over time with interactive charts
- ✅ **Analytics Dashboard** - Statistical analysis and trend visualization
- ✅ **Coping Strategy Tracker** - Log and rate personal coping techniques
- ✅ **Data Export** - Download screening data as CSV
- ✅ **Admin Dashboard** - Manage users and system statistics
- ✅ **Intelligent Recommendations** - AI-style personalized suggestions
- ✅ **Responsive Design** - Mobile-optimized beautiful UI
- ✅ **Complete Documentation** - 7 comprehensive guides

---

## 🚀 Quick Start

### **Installation**
```bash
pip install -r requirements.txt
```

### **Run the Application**
```bash
python app.py
```

### **Access the App**
Open browser: `http://localhost:5000`

### **Create Account**
1. Click "Register"
2. Enter username, email (optional), password
3. Login
4. Start taking assessments!

---

## 📚 Documentation

Read these guides in order:

| File | Purpose |
|------|---------|
| **START_HERE.md** | Quick orientation (start here!) |
| **QUICKSTART.md** | Step-by-step user guide |
| **SUMMARY.md** | 10-minute feature overview |
| **FEATURES_ADDED.md** | Detailed feature descriptions |
| **DOCUMENTATION.md** | Technical reference guide |
| **DEVELOPMENT.md** | Architecture and code notes |
| **IMPLEMENTATION.md** | Verification checklist |

---

## 🎯 Core Features

### **1. User Management**
- Register with email
- View/edit profile
- Change password
- Admin role support

### **2. Assessment System**
- Quick screening (3 questions)
- Extended assessment (10 questions)
- Risk level categorization
- Component score breakdown

### **3. Data Tracking**
- Complete screening history
- Interactive chart visualization
- Trend detection
- Assessment timestamps

### **4. Analytics**
- Statistical summary
- Risk distribution charts
- Trend analysis
- Intelligent insights

### **5. Coping Strategies**
- Log personal strategies
- Effectiveness ratings (1-5)
- Historical tracking
- Personal library

### **6. Data Management**
- CSV export
- Complete data backup
- Healthcare provider sharing

### **7. Admin Features**
- User management dashboard
- Role assignment
- System statistics
- User deletion

### **8. Security**
- Password hashing
- CSRF protection
- Admin route protection
- Session management
- Data validation

---

## 📁 Project Structure

```
Mental Health Platform/
├── app.py                    # Flask application (main)
├── models.py                 # Database models (SQLAlchemy)
├── forms.py                  # WTForms classes
├── requirements.txt          # Python dependencies
├── database.db              # SQLite database
├── static/
│   └── style.css            # CSS styling
├── templates/               # HTML templates (19 files)
│   ├── base.html            # Navigation template
│   ├── dashboard.html       # User dashboard
│   ├── profile.html         # User profile
│   ├── extended_screening.html
│   ├── analytics.html       # Analytics dashboard
│   ├── admin_dashboard.html # Admin panel
│   └── [10 other templates]
├── tests/                   # Test files
└── [Documentation files]    # 7 markdown guides
```

---

## 🛠️ Technologies Used

### **Backend**
- Flask 2.2+
- SQLAlchemy ORM
- Flask-Login
- Flask-WTF
- Werkzeug

### **Frontend**
- Bootstrap 5.3
- Chart.js
- HTML5/CSS3

### **Database**
- SQLite (local)
- PostgreSQL ready (production)

---

## 📊 Database Models

### **User** (Enhanced)
- username, email, password
- role, created_at, updated_at
- bio, preferences
- Relationships: screenings, coping_logs

### **Screening** (Enhanced)
- user_id, score, level
- created_at, notes
- Component scores (stress, anxiety, sleep, depression, social)
- Relationships: user, recommendations

### **CopingLog** (New)
- user_id, strategy, description
- effectiveness, created_at

### **Recommendation** (New)
- screening_id, category, title
- description, url

---

## 🔐 Security Features

✅ Password hashing with Werkzeug
✅ CSRF protection on all forms
✅ Admin route protection
✅ Session-based authentication
✅ Input validation
✅ Database cascade delete
✅ Admin self-deletion prevention

---

## 📡 API Routes (16 Total)

### **Authentication**
- `GET /register` - Registration form
- `POST /register` - Create account
- `GET /login` - Login form
- `POST /login` - Authenticate user
- `GET /logout` - Logout

### **Core Features**
- `GET /dashboard` - User dashboard
- `GET /screening` - Quick screening
- `POST /screening` - Process screening
- `GET /extended-screening` - Extended assessment
- `POST /extended-screening` - Process extended assessment
- `GET /awareness` - Awareness information
- `GET /support` - Support resources

### **User Management**
- `GET /profile` - View profile
- `GET /profile/edit` - Edit profile form
- `POST /profile/edit` - Update profile
- `GET /change-password` - Change password form
- `POST /change-password` - Update password

### **Data & Analytics**
- `GET /history` - Screening history
- `GET /analytics` - Analytics dashboard
- `GET /export-data` - Download CSV

### **Coping Strategies**
- `GET /coping-strategies` - View strategies
- `GET /log-strategy` - Log strategy form
- `POST /log-strategy` - Save strategy

### **Admin**
- `GET /admin` - Admin dashboard
- `POST /admin/users/<id>/toggle-admin` - Toggle role
- `POST /admin/users/<id>/delete` - Delete user

---

## 🎓 Usage Examples

### **Take an Assessment**
1. Login to your account
2. Click "Extended Assessment" in Tools menu
3. Answer 10 questions across 5 categories
4. Get instant results with recommendations

### **View Your Progress**
1. Click "Analytics" in Tools menu
2. See your statistics and trends
3. Download CSV if needed

### **Log a Coping Strategy**
1. Click "Coping Strategies" in Tools menu
2. Click "Log Strategy"
3. Describe what you did and rate effectiveness

### **Share with Doctor**
1. Click "View History" → "Export Data"
2. Send CSV file to healthcare provider

---

## 🧪 Testing

### **Run Tests**
```bash
pytest -q
```

### **Test Coverage**
- ✅ Authentication routes
- ✅ Assessment creation
- ✅ Profile management
- ✅ Admin features
- ✅ Data export

---

## 🐳 Docker (Optional)

### **Build and Run**
```bash
docker-compose up --build
```

### **Access**
```
http://localhost:5000
```

---

## 🚀 Deployment

### **Production Checklist**
- [ ] Set `DEBUG = False`
- [ ] Update `SECRET_KEY` to strong value
- [ ] Configure production database URL
- [ ] Set environment variables
- [ ] Enable HTTPS
- [ ] Configure CORS
- [ ] Set up monitoring

See **DEVELOPMENT.md** for detailed deployment guide.

---

## 🔄 Migrations (Optional)

If using Flask-Migrate:
```bash
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

---

## 📊 Sample Data

Create demo user:
```bash
python seed.py
```
Username: `demo`
Password: `demo123`

---

## 🎨 UI Features

- **Responsive Design**: Works on mobile, tablet, desktop
- **Interactive Charts**: Chart.js visualizations
- **Color-Coded Status**: Green/Yellow/Red risk levels
- **Progress Indicators**: Visual badges and statistics
- **Dropdown Navigation**: Easy access to all features
- **Mobile Menu**: Hamburger menu for mobile

---

## 🔧 Customization

### **Modify Assessment Questions**
Edit `ExtendedScreeningForm` in `forms.py`

### **Change Risk Levels**
Edit scoring logic in `app.py` routes

### **Update Styling**
Edit `static/style.css` or templates

### **Add New Models**
Add to `models.py` and create migration

---

## 📈 Statistics

| Metric | v1.0 | v2.0 |
|--------|------|------|
| Routes | 4 | 16 |
| Templates | 6 | 19 |
| Models | 2 | 4 |
| Assessment Questions | 3 | 3 + 10 |
| Features | Basic | Advanced |

---

## 🌟 Key Improvements

✨ Professional-grade application
✨ Advanced assessment system
✨ Comprehensive analytics
✨ User-friendly interface
✨ Complete documentation
✨ Production-ready code
✨ Security hardened
✨ Mobile optimized

---

## 📞 Support

### **User Questions**
→ Read **QUICKSTART.md**

### **Technical Questions**
→ Read **DOCUMENTATION.md**

### **Feature Details**
→ Read **FEATURES_ADDED.md**

### **Architecture**
→ Read **DEVELOPMENT.md**

---

## 📝 License

This project is provided as-is for mental health awareness and screening purposes.

---

## ⚠️ Disclaimer

This platform is for **educational and screening purposes only**. It is not a substitute for professional mental health care. If you or someone you know is struggling with mental health:

- **Call 988** (US Suicide & Crisis Lifeline)
- **Text HOME to 741741** (Crisis Text Line)
- **Seek professional help** from a licensed mental health provider

---

## 🎉 Getting Started

1. **Read**: START_HERE.md
2. **Install**: `pip install -r requirements.txt`
3. **Run**: `python app.py`
4. **Access**: `http://localhost:5000`
5. **Register**: Create account
6. **Explore**: Try the features!

---

## 📚 Documentation Files

| File | Length | Purpose |
|------|--------|---------|
| START_HERE.md | Quick | Quick start guide |
| QUICKSTART.md | Medium | Step-by-step user guide |
| SUMMARY.md | Medium | Feature overview |
| FEATURES_ADDED.md | Long | Detailed features |
| DOCUMENTATION.md | Long | Technical reference |
| DEVELOPMENT.md | Long | Architecture notes |
| IMPLEMENTATION.md | Long | Verification |

---

**Version**: 2.0 Advanced Edition
**Status**: ✅ Production Ready
**Last Updated**: February 2026

**🧠 Your mental health assessment platform is ready to use!**