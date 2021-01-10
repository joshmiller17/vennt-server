import requests, json, uuid

url = 'http://localhost:3004/'

# create a new account
username = str(uuid.uuid4())
data = '{"register": "%s", "password": "pw"}' % username
response = requests.post(url, data=data.encode('utf-8'))
print(response.text)

# login
data = '{"login": "%s", "password": "pw"}' % username
response = requests.post(url, data=data.encode('utf-8'))
print(response.text)

response = json.loads(response.text)
auth_token = response["auth_token"]

# create a new character
response = requests.get(url + 'create_character?q={"auth_token":"%s","name":"myfirstcharacter"}' % auth_token)
print(response.text)