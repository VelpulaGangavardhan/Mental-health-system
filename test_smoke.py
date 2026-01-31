import requests
s = requests.Session()
base = 'http://127.0.0.1:5000'
# login
resp = s.post(base + '/login', data={'username':'demo','password':'demo123'})
print('login ->', resp.status_code, resp.url)
# dashboard
resp = s.get(base + '/dashboard')
print('dashboard ->', resp.status_code)
# screening
resp = s.post(base + '/screening', data={'q1':'2','q2':'1','q3':'0'})
print('screening ->', resp.status_code)
print('result page contains Score ->', 'Score' in resp.text)
