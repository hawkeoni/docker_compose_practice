import requests
from utils import generate_fake_tweet

resp = requests.post("http://172.22.0.3:6000/inference", json=generate_fake_tweet(["aaaaaa", "bbbbbb", "cccccccc"]))
print(resp.status_code)
if resp.status_code == 200:
    print(resp.json())
