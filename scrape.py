#environemnt information
from dotenv import load_dotenv
load_dotenv()

import requests
import time
import json
import os

time.sleep(15)

eia_doc = str(requests.get("http://ir.eia.gov/ngs/wngsr.json").content) # makes request for EIA json
eia_str = eia_doc[eia_doc.find("{"):-1] # splices the string-request by the first known open bracket
eia_rev = eia_str[::-1] # reverses the string
end_loc = eia_rev.find("}") # finds the negative index of the closing bracket
eia_str = eia_str[:-end_loc] # splices original string to squeeze out open and close brackets
eia_json = json.loads(eia_str) # loads the string into JSON
injection = eia_json["series"][0]["calculated"]["net_change"] # traverses JSON to find delta change (injection)
injection = int(injection) # ensures the number is an integer
release_date = eia_json["current_week"]

text = "<@&849420131947511839> EIA Supply results are in!"
if injection > 0:
    text += f" We have injected **{injection}** billion cubic feet from supplies "
elif injection == 0:
    text += f" There was no net change to the supplies "
else:
    text += f" We have withdrawn **{injection*-1}** billion cubic feet from supplies "
text += f"for the week ending {release_date}"

requests.post(os.getenv("WEBHOOK"), data={"content": text})
