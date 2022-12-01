from urllib import response
import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"likes": 10, "name": "video1", "views": 100},
    {"likes": 20, "name": "video2", "views": 200},
    {"likes": 30, "name": "video3", "views": 300}
]

for i in range(len(data)):
    response = requests.put(f"{BASE}video/{i}", data[i])
    print(response.json())

input()
for i in range(len(data)):
    response = requests.get(f"{BASE}video/{i}")
    print(response.json())

input()
response = requests.get(f"{BASE}video/6")
print(response.json())