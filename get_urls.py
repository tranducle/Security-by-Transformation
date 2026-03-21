import urllib.request
import urllib.parse
import re

queries = [
    "Moffatt v. Air Canada 2024 BCCRT 149 canlii",
    "McCarthy Tétrault Air Canada Chatbot Decision",
    "Forbes What Air Canada Lost In The Remarkable AI Chatbot Case",
    "TechTarget AI prompt injection explained",
    "CyberNews Chevy Tahoe 1 dollar chatgpt bot hack",
    "Towards Data Science Prompt Injection in Large Language Models",
    "The Register Samsung bans ChatGPT",
    "ISACA the samsung chatgpt leak what it means for corporate security",
    "Cyberhaven 11 percent of employee prompts to chatgpt contain sensitive information"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for q in queries:
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'class="result__url" href="([^"]+)"', html)
        if match:
            # DuckDuckGo sometimes wraps URLs in a redirect
            res_url = match.group(1)
            if "uddg=" in res_url:
                res_url = urllib.parse.unquote(res_url.split("uddg=")[1].split("&")[0])
            print(f"QUERY: {q}\nURL: {res_url}\n")
        else:
            print(f"QUERY: {q}\nURL: Not found\n")
    except Exception as e:
        print(f"QUERY: {q}\nError: {e}\n")
