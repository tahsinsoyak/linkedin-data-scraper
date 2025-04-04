import urllib.request
import time
import json
from string import ascii_lowercase
from itertools import product

URL = "https://www.linkedin.com/skill?query="

def get_skills(query_suffix):
    with urllib.request.urlopen(URL + query_suffix) as response:
        json_skills = response.read().decode('utf-8')
        if not json_skills.strip():  # Check if the response is empty
            return []
        try:
            dictionary_skills = json.loads(json_skills)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for query '{query_suffix}': {json_skills[:100]}")
            return []
    return [skill['displayName'] for skill in dictionary_skills.get('resultList', [])]

with open('linkedin_skills.txt', 'w') as file:
    for triple in product(*(ascii_lowercase,)*3):
        time.sleep(0.1)
        ret = get_skills(''.join(triple))
        file.write('\n'.join(ret) + '\n')
