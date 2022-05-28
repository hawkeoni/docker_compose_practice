import requests
resp = requests.post("http://172.18.0.3:6000/inference", json={"a": "b", "text": "some tweet"})
print(resp.status_code)
if resp.status_code == 200:
    print(resp.json())
