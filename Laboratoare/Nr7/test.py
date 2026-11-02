import requests

BASE = "https://httpbin.org"

PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]

def post_json(data):
    r = requests.post(BASE + "/post", json=data)
    return r.json()["json"]


def post_form(data):
    r = requests.post(BASE + "/post", data=data)
    return r.json()["form"]

 # Partea 3
print("\nPartea 3")

print(post_json({
        "name": "Ana",
        "age": 19,
        "tags": ["a", "b"]
    }))

print(post_form({
        "user": "ana",
        "city": "Bălți"
    }))