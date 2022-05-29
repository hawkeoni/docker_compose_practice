import requests
from utils import generate_fake_tweet
from pprint import pprint
from string import ascii_letters
import random

fake_tweet = generate_fake_tweet(["".join(random.choices(ascii_letters, k=10))])
pprint(fake_tweet)
resp = requests.post("http://172.24.0.6:6000/inference", json=fake_tweet)
print(resp.status_code)
if resp.status_code == 200:
    print(resp.json())
