import requests
from packages.includes import write

header = {"Host":"evil.com"}

def cvescan(url,output):
    try:
        req = requests.get(url,headers=header,timeout=5)
        responce = req.url
        if "evil.com" in responce:
            print(f"\nit's Vuln: {url}")
            if output is not None:
                write.write(output,str(url+'\n'))
        else:
            print(f"not Vuln: {url}\n")
    except requests.exceptions.RequestException as e:
        print("invalid url")
