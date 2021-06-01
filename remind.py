#environemnt information
from dotenv import load_dotenv
load_dotenv()

import requests
import os

text = "EIA in 10 minutes!"
requests.post(os.getenv("WEBHOOK"), data={"content": text})
