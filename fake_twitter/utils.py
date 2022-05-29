import time
import json
import uuid
import random
from string import ascii_letters
from typing import Dict, Any, List

from countries import countries

static = json.load(open("/static/static.json"))

def generate_fake_tweet() -> Dict[str, Any]:
    return {
        "tweet_id": str(uuid.uuid4()),
        "username": random.choice(static["users"]), 
        "country": random.choice(countries),
        "text": random.choice(static["texts"]),
        "time": int(time.time()),
        "verified": bool(random.randint(0, 1)),
        "followers": random.randint(0, 10000),
        }
