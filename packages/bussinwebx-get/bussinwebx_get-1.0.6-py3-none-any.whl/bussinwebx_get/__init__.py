import requests
import json

def getip(domain, tld):
    """
    Gets IP/github root of a BUSS/webx domain.
    
    Parameters:
    domain (string): The first part of the domain (ex: example for example.dev)
    tld (string): The second part of the domain, the Top Level Domain (ex: dev for example.dev)
    
    Returns:
    string: the IP or github root of the BUSS/webx domain.
    """
    buss = requests.get(f"https://api.buss.lol/domain/{domain}/{tld}")
    if buss.status_code == 429:
        raise Exception('Ratelimit for BUSS (webx)')
    elif buss.status_code == 404:
        raise Exception('BUSS (webx) Domain does not exist')
    elif buss.status_code == 200:
        return json.loads(buss.text)["ip"]
    else:
        raise Exception('BUSS (webx): Unknown Error')

def get(domain: str, tld: str, path="/"):
    """
    Preforms a HTTP request on a BUSS/webx domain.
    
    Parameters:
    domain (string): The first part of the domain (ex: example for example.dev)
    tld (string): The second part of the domain, the Top Level Domain (ex: dev for example.dev)
    path (string): The path of the domain. Defaults to "/".

    Returns:
    requests.Response: the HTTP request.
    """
    bussip = getip(domain, tld)
    if bussip.startswith("https://github.com"):
        raw_url = bussip.replace("https://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + f'/main/' + '/'.join(parts[5:])
        if path=="/":
            return requests.get(f"{raw_url}/index.html")
        else:
            return requests.get(f"{raw_url}{path}")
    if bussip.startswith("http://github.com"):
        raw_url = bussip.replace("http://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + f'/main/' + '/'.join(parts[5:])
        if path=="/":
            return requests.get(f"{raw_url}/index.html")
        else:
            return requests.get(f"{raw_url}{path}")
    else:
        return requests.get(f"{bussip}{path}")