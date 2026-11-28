# web-scout-light/SKILL.md
Basic web search using Tavily API.
# web-scout-light/run.py
import os, requests, ast
def search(query):
    key = os.getenv('TAVILY_API_KEY')
    r = requests.post('https://api.tavily.com/search', json={'api_key': key, 'query': query, 'search_depth': 'basic', 'max_results': 3})
    return r.json()['results']
# Validate
ast.parse(open(__file__).read())