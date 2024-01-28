import requests


url = "https://explv-map.siisiqf.workers.dev/"
body = {
    "start": {"x": 3108, "y": 3318, "z": 0},
    "end": {"x": 3023, "y": 3408, "z": 0},
    "player": {"members": "false"}
}

result = requests.post(url, json=body, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Origin': 'https://explv.github.io',
    'Connection': 'keep-alive',
    'Referer': 'https://explv.github.io/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'TE': 'trailers'
})

print(result.text)
