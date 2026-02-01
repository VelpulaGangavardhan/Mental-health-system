# Quick Start Guide - Advanced Features

## Getting Started

### 1. **Installation**
```bash
pip install -r requirements.txt
python app.py
```

Visit: `http://localhost:5000`

---

## Feature Walkthrough

### User Account Setup
1. **Register**: Click "Register" → Enter username, email (optional), and password
2. **Confirm Password**: Verify your password matches
3. **Login**: Use username or email to log in

### Dashboard Overview
After logging in, you'll see:
- **Welcome Message**: Personalized greeting with your username
- **Key Metrics**: Total screenings, average score, account creation date
- **Recent Screenings**: Table showing your last assessments
- **Quick Action Buttons**: Easy access to all features

### Taking Assessments

#### Quick Screening (3 questions - ~2 minutes)
1. Click **"Quick Screening"** on dashboard
2. Answer 3 questions about stress, anxiety, and sleep
3. View instant results with score and risk level
4. Get personalized recommendations

#### Extended Assessment (10 questions - ~5 minutes)
1. Click **"Extended Assessment"** on dashboard
2. Answer questions across 5 categories:
   - Stress Management
   - Anxiety Levels
   - Sleep Quality
   - Depression Indicators
   - Social Support
3. Add optional notes
4. Receive detailed breakdown with component scores
5. Get category-specific recommendations

### Viewing Your Data

#### Screening History
- Click **"View History"** in Tools menu
- See all past screenings with dates and scores
- **Trend Indicator**: Shows if you're improving, worsening, or stable
- **Chart Visualization**: Interactive line chart of your score progression
- **Export Data**: Download as CSV for external analysis

#### Analytics Dashboard
- Click **"Analytics"** in Tools menu
- **Key Stats**:
  - Total screenings taken
  - Average score calculation
  - Score range (lowest to highest)
  - Overall trend analysis
  - Last screening date
- **Risk Distribution**: Visual breakdown of Low/Moderate/High results
- **Insights**: AI-generated recommendations based on your data
- **Alerts**: Warnings if concerning patterns detected

### Managing Coping Strategies

#### Log a Strategy
1. Click **"Log Strategy"** in Tools menu or from assessment results
2. Enter strategy name (e.g., "Deep breathing")
3. Describe how you used it and results
4. Rate effectiveness (1-5 stars)
5. Save to your personal strategy library

#### View Strategies
- Click **"Coping Strategies"** in Tools menu
- See all strategies you've logged
- **Effectiveness Indicator**: Stars show how well it worked
- **Filter**: Strategies ordered by recency

### Managing Your Profile

#### View Profile
- Click **"Profile"** in Tools menu
- See your account information:
  - Username
  - Email
  - Member since date
  - Total screenings completed
  - Bio (if added)

#### Edit Profile
1. Click **"Edit Profile"** button
2. Update username, email, or add bio
3. Submit changes
4. Changes saved immediately

#### Change Password
1. Click **"Change Password"** button
2. Enter current password (verification)
3. Enter new password
4. Confirm new password
5. Submit to save

### Exporting Your Data

1. Click **"View History"** → **"Export Data"** button
2. CSV file downloads with filename: `screening_data_YYYYMMDD.csv`
3. Includes all your screening data with component scores
4. Open in Excel, Google Sheets, or data analysis tools

---

## Admin Features (Admin Users Only)

### Accessing Admin Panel
1. Click **"Admin"** link in Tools dropdown (only visible to admins)
2. View system-wide statistics
3. Manage all user accounts

### User Management
- **View All Users**: See username, email, role, join date
- **Toggle Admin**: Promote users to admin or demote to regular user
- **Delete Users**: Remove accounts (cannot delete yourself)
- **User Statistics**: See average screenings per user

---

## Tips & Best Practices

### For Better Insights
✅ Take assessments regularly (weekly recommended)
✅ Be honest in your answers
✅ Add notes to important screenings
✅ Log coping strategies that work for you
✅ Track which strategies are most effective

### Data Management
✅ Export your data monthly for backup
✅ Review your history periodically
✅ Look for patterns in your scores
✅ Check analytics insights for guidance

### Personal Wellness
✅ Use high effectiveness strategies consistently
✅ Seek professional help for high-risk scores
✅ Share results with healthcare providers
✅ Update your profile regularly

---

## Support Information

If you're experiencing high stress or anxiety:
- **988 Suicide & Crisis Lifeline**: Call or text 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **International Hotlines**: Available in most countries
- **Professional Help**: Consult a mental health provider

---

## Common Questions

**Q: Can I export my data?**
A: Yes! Click "Export Data" from history page to download CSV.

**Q: What do the risk levels mean?**
- Low: Generally good mental health, continue current practices
- Moderate: Some concerns, consider coping strategies or professional support
- High: Significant concerns, strongly recommend professional help

**Q: How are component scores calculated?**
Each category has 2 questions scored 0-2, giving category scores of 0-4.

**Q: Can I delete my account?**
Contact an admin to request account deletion.

**Q: Are my results private?**
Yes! Your data is personal and only visible to you (and admins if you're an admin).

---

## Navigation Quick Links

| Feature | Path |
|---------|------|
| Dashboard | `/dashboard` |
| Quick Screening | `/screening` |
| Extended Assessment | `/extended-screening` |
| Screening History | `/history` |
| Analytics | `/analytics` |
| Coping Strategies | `/coping-strategies` |
| Profile | `/profile` |
| Export Data | `/export-data` |
| Admin Panel | `/admin` |

---

## Keyboard Shortcuts (Future Feature)

Coming soon! Common tasks will have keyboard shortcuts for power users.

---

**Version**: 2.0 Advanced Edition
**Last Updated**: February 2026
