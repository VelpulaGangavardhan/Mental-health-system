# Development Notes & Architecture

## Implementation Summary

### Changes Made

#### **models.py** - Database Models
- **Enhanced User Model**:
  - Added `email` field (unique)
  - Added `role` field (user/admin)
  - Added `created_at` and `updated_at` timestamps
  - Added `bio` and `preferences` fields
  - Added relationship to `CopingLog`

- **Enhanced Screening Model**:
  - Added `created_at` timestamp
  - Added `notes` field
  - Added individual component scores:
    - `stress_score`
    - `anxiety_score`
    - `sleep_score`
    - `depression_score`
    - `social_score`
  - Added relationship to `Recommendation`

- **New CopingLog Model**:
  - Tracks user-logged coping strategies
  - Stores effectiveness rating (1-5)
  - Associates with User via foreign key

- **New Recommendation Model**:
  - Stores personalized recommendations
  - Categories: professional, coping, resource
  - Linked to specific screenings

#### **forms.py** - WTForm Classes
- **Enhanced RegisterForm**:
  - Added email field
  - Added password confirmation
  
- **New ExtendedScreeningForm**:
  - 10 radio button fields (2 per category)
  - 5 assessment categories
  - Optional notes textarea

- **New ProfileForm**:
  - Username, email, bio fields
  - Validation for each field

- **New ChangePasswordForm**:
  - Current password verification
  - New password with confirmation
  - Password strength validation

- **New CopingLogForm**:
  - Strategy name (string)
  - Description (textarea)
  - Effectiveness rating (select 1-5)

#### **app.py** - Flask Routes & Logic
- **New Decorators**:
  - `@admin_required` - Protects admin-only routes

- **Enhanced Authentication**:
  - Login now accepts email or username
  - Registration includes email validation
  - Email uniqueness check

- **New Routes** (12 new endpoints):
  - User Management:
    - `/profile` - View profile
    - `/profile/edit` - Edit profile
    - `/change-password` - Change password
  
  - Assessments:
    - `/extended-screening` - Extended assessment
  
  - Data Tracking:
    - `/history` - Screening history
    - `/analytics` - Analytics dashboard
    - `/export-data` - CSV export
  
  - Strategies:
    - `/coping-strategies` - View strategies
    - `/log-strategy` - Log new strategy
  
  - Admin:
    - `/admin` - Admin dashboard
    - `/admin/users/<id>/toggle-admin` - Role management
    - `/admin/users/<id>/delete` - User deletion

- **Core Logic**:
  - `get_recommendations()` - Dynamic recommendation engine
  - Risk-level based scoring
  - Trend analysis and calculation
  - CSV generation and download

#### **templates/** - New HTML Templates (12 new files)
1. **profile.html** - User profile display
2. **edit_profile.html** - Profile edit form
3. **change_password.html** - Password change form
4. **extended_screening.html** - Extended assessment form
5. **extended_result.html** - Assessment results with breakdown
6. **screening_history.html** - History with Chart.js graph
7. **analytics.html** - Analytics with doughnut chart
8. **coping_strategies.html** - Strategy list view
9. **log_strategy.html** - Strategy logging form
10. **admin_dashboard.html** - Admin management panel
11. **base.html** (modified) - Added dropdown navigation
12. **dashboard.html** (modified) - Enhanced dashboard

---

## Architecture Decisions

### 1. **Database Design**
- **Normalization**: Each model represents a single entity
- **Relationships**: Foreign keys link related data
- **Cascade Delete**: User deletion removes all related data
- **Timestamps**: Track when records are created/modified

### 2. **Security**
- **Password Hashing**: Werkzeug `generate_password_hash`
- **Session Management**: Flask-Login handles authentication
- **CSRF Protection**: Flask-WTF forms include tokens
- **Role-Based Access**: Admin decorator enforces permissions
- **Input Validation**: All forms validated server-side

### 3. **Frontend Architecture**
- **Bootstrap 5**: Responsive grid layout
- **Chart.js**: Interactive data visualization
- **Mobile-First**: Responsive design on all templates
- **Accessibility**: Semantic HTML with proper labels

### 4. **Code Organization**
- **Separation of Concerns**: Models, Forms, Routes separate
- **DRY Principle**: Reusable templates (base.html)
- **Modular Routes**: Related routes grouped logically
- **Helper Functions**: `get_recommendations()` extracted

---

## Feature Implementation Details

### **Scoring System**
```python
# Extended Screening Scoring
Stress Score: q1 + q2 (0-4)
Anxiety Score: q1 + q2 (0-4)
Sleep Score: q1 + q2 (0-4)
Depression Score: q1 + q2 (0-4)
Social Score: q1 + q2 (0-4)
Total Score: Sum of all components (0-20)

Risk Levels:
- Low: 0-15
- Moderate: 16-30
- High: 31-50
```

### **Recommendation Engine**
```python
# Dynamic recommendations based on risk level
def get_recommendations(score, level, screening_id):
    if level == 'High':
        # Professional support + crisis resources
    elif level == 'Moderate':
        # Coping techniques + wellness resources
    else:  # Low
        # Maintenance strategies
```

### **Trend Analysis**
```python
# Compare latest vs oldest screening
if latest_score < oldest_score:
    trend = 'Improving'
elif latest_score > oldest_score:
    trend = 'Worsening'
else:
    trend = 'Stable'
```

---

## Data Flow Diagrams

### **Assessment Flow**
```
User → Extended Assessment Form
    ↓
Form Validation
    ↓
Calculate Scores
    ↓
Determine Risk Level
    ↓
Generate Recommendations
    ↓
Save to Database
    ↓
Display Results
```

### **Analytics Flow**
```
Database Query Screenings
    ↓
Calculate Statistics
    ↓
Analyze Trends
    ↓
Generate Insights
    ↓
Build Charts
    ↓
Display Dashboard
```

### **Export Flow**
```
Query User Screenings
    ↓
Format as CSV
    ↓
Create StringIO Buffer
    ↓
Send as Download
    ↓
User receives screening_data_YYYYMMDD.csv
```

---

## Performance Considerations

### **Database Queries**
- Indexed lookups on `user_id` and `username`
- Efficient sorting by `created_at`
- Cascade delete prevents orphaned records
- Lazy loading relationships to reduce memory

### **Caching Opportunities**
- Cache user dashboard stats (1 hour TTL)
- Cache analytics calculations
- Cache recommendation library

### **Scaling Considerations**
- Switch to PostgreSQL for production
- Add database indexing on frequently queried fields
- Implement query pagination for large datasets
- Use celery for async tasks (exports, emails)

---

## Testing Recommendations

### **Unit Tests to Add**
```python
# Model tests
def test_user_password_hashing()
def test_screening_score_calculation()
def test_coping_log_effectiveness()

# Form tests
def test_profile_form_validation()
def test_extended_screening_form()
def test_password_change_validation()

# Route tests
def test_profile_view_requires_login()
def test_admin_route_requires_admin()
def test_export_data_format()
def test_analytics_calculations()
```

### **Integration Tests**
- User registration → login → assessment flow
- Admin user management → role toggle → user deletion
- Data export → CSV validation
- Strategy logging → effectiveness rating

---

## Future Enhancement Opportunities

### **Short Term** (v2.1)
- [ ] Email notifications for high-risk screenings
- [ ] Password reset via email
- [ ] User profile pictures
- [ ] Custom assessment questionnaires
- [ ] Search and filter screenings

### **Medium Term** (v2.5)
- [ ] Peer support groups/forums
- [ ] Integration with calendar
- [ ] Mobile app (React Native)
- [ ] API for third-party integrations
- [ ] Advanced data analytics (pandas, matplotlib)

### **Long Term** (v3.0)
- [ ] AI-powered chatbot support
- [ ] Machine learning for trend prediction
- [ ] Video/voice assessment options
- [ ] Integration with wearables
- [ ] Multi-language support
- [ ] Telehealth provider connections
- [ ] Insurance integration

---

## Deployment Checklist

### **Pre-Deployment**
- [ ] Set `DEBUG = False`
- [ ] Update `SECRET_KEY` to strong value
- [ ] Configure production database URL
- [ ] Set up environment variables
- [ ] Run all tests
- [ ] Test on staging environment

### **Database Migration**
- [ ] Backup existing database
- [ ] Run migrations if any
- [ ] Verify new models created
- [ ] Create admin account(s)

### **Security**
- [ ] Enable HTTPS
- [ ] Configure CORS policies
- [ ] Set up rate limiting
- [ ] Enable CSRF protection
- [ ] Configure password requirements

### **Monitoring**
- [ ] Set up logging
- [ ] Configure error tracking
- [ ] Monitor database performance
- [ ] Track user activity
- [ ] Set up alerts for errors

---

## Configuration Options

### **Environment Variables**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
FLASK_DEBUG=0
```

### **App Config**
```python
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
```

---

## Code Quality Standards

### **Followed**
- PEP 8 style guidelines
- Docstring comments on functions
- Meaningful variable names
- DRY (Don't Repeat Yourself)
- SOLID principles

### **Recommended Additions**
- Type hints for function parameters
- More detailed docstrings
- Logging statements
- Error handling with try-except

---

## Git Commit Messages (Suggested)

```
feat: Add user profile management
feat: Implement extended assessment system
feat: Add analytics dashboard with charts
feat: Add coping strategy tracking
feat: Implement admin user management
feat: Add data export functionality
refactor: Reorganize routes by feature
docs: Add comprehensive documentation
test: Add unit tests for models
```

---

## Dependencies Review

### **Current**
- Flask 2.2+ ✅
- SQLAlchemy ✅
- Flask-Login ✅
- Flask-WTF ✅
- Werkzeug ✅
- Python-dotenv ✅
- pytest/pytest-flask ✅
- Pillow (new)
- pandas (new)
- matplotlib (optional)

### **Future Considerations**
- Celery for task queue
- Redis for caching
- Alembic for migrations
- Gunicorn for production
- Nginx reverse proxy

---

## Version History

### **v1.0 - Original**
- Basic authentication
- Quick screening (3 questions)
- Simple dashboard
- Results display

### **v2.0 - Advanced** (Current)
- Enhanced user management
- Extended assessment (10 questions)
- Screening history with charts
- Analytics dashboard
- Coping strategy tracking
- Data export
- Admin panel
- Improved navigation

### **v2.1 - Planned**
- Email notifications
- Password reset
- User avatars
- Custom assessments

---

## Notes for Future Developers

1. **Database Migrations**: Consider Alembic for schema changes
2. **Testing**: Expand test coverage to 80%+
3. **Documentation**: Keep docstrings updated with code
4. **Security**: Regular security audits recommended
5. **Performance**: Monitor query performance with SQL logging
6. **User Feedback**: Implement feedback collection system

---

**Last Updated**: February 2026
**Maintained By**: Development Team
**Status**: Production Ready
