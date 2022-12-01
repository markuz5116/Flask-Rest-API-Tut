from urllib import response
import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "video/1", {"likes": 10, "name": "hello world", "views": 100})
print(response.json())
