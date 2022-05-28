import requests
resp = requests.post("http://127.0.0.1:5000/inference", json={"a": "b", "text": "some tweet"})
print(resp.status_code)
if resp.status_code == 200:
    print(resp.json())
