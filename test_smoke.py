"""
Smoke Tests for Mental Health Platform
Tests all major user flows end-to-end
"""
import requests
import sys

def run_smoke_tests():
    s = requests.Session()
    base = 'http://127.0.0.1:5000'
    
    print("\n=== MENTAL HEALTH PLATFORM SMOKE TESTS ===\n")
    
    # Test 1: Register new user
    print("Test 1: User Registration")
    resp = s.post(base + '/register', data={
        'username': 'smoketest_user',
        'email': 'smoke@test.com',
        'password': 'smokepw123',
        'confirm_password': 'smokepw123'
    })
    print(f"  Register -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 2: Login with username
    print("Test 2: Login with Username")
    resp = s.post(base + '/login', data={
        'username': 'smoketest_user',
        'password': 'smokepw123'
    })
    print(f"  Login -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 3: Access dashboard
    print("Test 3: Dashboard Access")
    resp = s.get(base + '/dashboard')
    print(f"  Dashboard -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 4: Quick screening
    print("Test 4: Quick Screening")
    resp = s.post(base + '/screening', data={
        'q1': '2',
        'q2': '1',
        'q3': '0'
    })
    print(f"  Screening -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    if 'score' not in resp.text.lower() and 'result' not in resp.text.lower():
        print(f"  ❌ FAILED: Result page missing score/result")
        return False
    print("  ✅ PASSED\n")
    
    # Test 5: Extended screening
    print("Test 5: Extended Screening")
    resp = s.post(base + '/extended-screening', data={
        'stress_q1': '2',
        'stress_q2': '1',
        'anxiety_q1': '1',
        'anxiety_q2': '0',
        'sleep_q1': '2',
        'sleep_q2': '2',
        'depression_q1': '1',
        'depression_q2': '0',
        'social_q1': '1',
        'social_q2': '1',
        'notes': 'Smoke test notes'
    })
    print(f"  Extended Screening -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 6: View screening history
    print("Test 6: Screening History")
    resp = s.get(base + '/history')
    print(f"  History -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 7: View analytics
    print("Test 7: Analytics Dashboard")
    resp = s.get(base + '/analytics')
    print(f"  Analytics -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 8: View profile
    print("Test 8: User Profile")
    resp = s.get(base + '/profile')
    print(f"  Profile -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 9: Log coping strategy
    print("Test 9: Log Coping Strategy")
    resp = s.post(base + '/log-strategy', data={
        'strategy': 'Deep breathing',
        'description': 'Practiced for 5 minutes',
        'effectiveness': '4'
    })
    print(f"  Log Strategy -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 10: View coping strategies
    print("Test 10: View Coping Strategies")
    resp = s.get(base + '/coping-strategies')
    print(f"  Coping Strategies -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 11: Export data
    print("Test 11: Export Data")
    resp = s.get(base + '/export-data')
    print(f"  Export -> {resp.status_code}")
    if resp.status_code != 200:
        print(f"  ❌ FAILED: Expected 200, got {resp.status_code}")
        return False
    if 'text/csv' not in resp.headers.get('Content-Type', ''):
        print(f"  ❌ FAILED: Not CSV format")
        return False
    print("  ✅ PASSED\n")
    
    # Test 12: Edit profile
    print("Test 12: Edit Profile")
    resp = s.post(base + '/profile/edit', data={
        'username': 'smoketest_user',
        'email': 'newemail@test.com',
        'bio': 'Updated bio'
    })
    print(f"  Edit Profile -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 13: Change password
    print("Test 13: Change Password")
    resp = s.post(base + '/change-password', data={
        'current_password': 'smokepw123',
        'new_password': 'newsmokepw123',
        'confirm_password': 'newsmokepw123'
    })
    print(f"  Change Password -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 14: Logout
    print("Test 14: Logout")
    resp = s.get(base + '/logout')
    print(f"  Logout -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 15: Login with new password
    print("Test 15: Login with New Password")
    resp = s.post(base + '/login', data={
        'username': 'smoketest_user',
        'password': 'newsmokepw123'
    })
    print(f"  Login with new password -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    # Test 16: Unauthenticated user cannot access dashboard
    print("Test 16: Dashboard Requires Auth")
    s.cookies.clear()  # Clear session
    resp = s.get(base + '/dashboard')
    print(f"  Dashboard (no auth) -> {resp.status_code}")
    if resp.status_code != 302:
        print(f"  ❌ FAILED: Expected 302 redirect, got {resp.status_code}")
        return False
    print("  ✅ PASSED\n")
    
    print("\n=== ALL SMOKE TESTS PASSED ===\n")
    return True

if __name__ == '__main__':
    try:
        success = run_smoke_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error running smoke tests: {str(e)}")
        print(f"Make sure the Flask app is running: python app.py")
        sys.exit(1)
