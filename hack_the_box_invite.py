import requests

h = { 'User-agent': 'Mozilla 5.0'}
u = "https://www.hackthebox.eu/api/invite/generate"
r = requests.post(u, headers=h)
print(r.text)