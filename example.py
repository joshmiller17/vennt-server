import requests

url = 'http://localhost:3004/'
data = b'{"register": "josh", "password": "pw"}'
response = requests.post(url, data=data)

print(response.text)