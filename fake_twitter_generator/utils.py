import time
import uuid
import random
from string import printable
from typing import Dict, Any, List

from countries import countries


def generate_fake_tweet(texts: List[str]) -> Dict[str, Any]:
    username = "".join(random.choice(printable, k=random.randint(5, 20)))
    text = random.choice(texts)

    return {
        "tweet_id": str(uuid.uuid4()),
        "username": username, 
        "country": random.choice(countries),
        "text": text,
        "time": int(time.time()),
        "verified": bool(random.randint(0, 1)),
        "followers": random.randint(0, 10000),
        }
