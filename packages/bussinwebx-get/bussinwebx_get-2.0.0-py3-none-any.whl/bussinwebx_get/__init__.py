import requests
import json

version="2.0.0"

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

def get(domain: str, tld: str, path="/", reportIfGithub=False, **kwards):
    """
    Preforms a HTTP request on a BUSS/webx domain.
    
    Parameters:
        domain (string): The first part of the domain (ex: example for example.dev)
        tld (string): The second part of the domain, the Top Level Domain (ex: dev for example.dev)
        path (string): The path of the domain. Defaults to "/".
        reportIfGithub (bool): If set to True, then if the domain is a github repo, raise an Exception for the reason shown below:
        Any other argument supported in requests.get are supported UNLESS IT IS A GITHUB REPO.

    Returns:
        requests.Response: the HTTP request.
    """
    bussip = getip(domain, tld)
    if bussip.startswith("https://github.com"):
        if reportIfGithub==True:
            raise Exception(f'BUSS (webx) Domain is Github Repo: \nDomain: {domain+"."+tld}\nOther arguments: {kwards}')
        raw_url = bussip.replace("https://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + '/main/'.join(parts[5:])
        if path=="/":
            return requests.get(f"{raw_url}/index.html")
        else:
            return requests.get(f"{raw_url}{path}")
    if bussip.startswith("http://github.com"):
        raw_url = bussip.replace("http://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + '/main/'.join(parts[5:])
        if path=="/":
            return requests.get(f"{raw_url}/index.html")
        else:
            return requests.get(f"{raw_url}{path}")
    else:
        return requests.get(f"{bussip}{path}", kwards)

def geturl(domain: str, tld: str, path="/"):
    """
    Preforms getip() with the addition of any path and conversts github.com to raw.githubusercontent.com.
    This could be used with requests.post or requests.put or any other http function to do said function.
    
    Parameters:
        domain (string): The first part of the domain (ex: example for example.dev)
        tld (string): The second part of the domain, the Top Level Domain (ex: dev for example.dev)
        path (string): The path of the domain. Defaults to "/".

    Returns:
        string: the URL.
    """
    bussip = getip(domain, tld)
    if bussip.startswith("https://github.com"):
        raw_url = bussip.replace("https://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + '/main/'.join(parts[5:])
        if path=="/":
            return f"{raw_url}/index.html"
        else:
            return f"{raw_url}{path}"
    if bussip.startswith("http://github.com"):
        raw_url = bussip.replace("http://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + '/main/'.join(parts[5:])
        if path=="/":
            return f"{raw_url}/index.html"
        else:
            return f"{raw_url}{path}"
    else:
        return f"{bussip}{path}"



def post(domain: str, tld: str, path="/", reportIfGithub=False, **kwards):
    """
    Preforms a HTTP POST request on a BUSS/webx domain.
    
    Parameters:
        domain (string): The first part of the domain (ex: example for example.dev)
        tld (string): The second part of the domain, the Top Level Domain (ex: dev for example.dev)
        path (string): The path of the domain. Defaults to "/".
        reportIfGithub (bool): If set to True, then if the domain is a github repo, raise an Exception for the reason shown below:
        Any other argument supported in requests.get are supported UNLESS IT IS A GITHUB REPO.

    Returns:
        requests.Response: the HTTP request.
    """
    bussip = getip(domain, tld)
    if bussip.startswith("https://github.com"):
        if reportIfGithub==True:
            raise Exception(f'BUSS (webx) Domain is Github Repo: \nDomain: {domain+"."+tld}\nOther arguments: {kwards}')
        raw_url = bussip.replace("https://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + '/main/'.join(parts[5:])
        if path=="/":
            return requests.post(f"{raw_url}/index.html")
        else:
            return requests.post(f"{raw_url}{path}")
    if bussip.startswith("http://github.com"):
        raw_url = bussip.replace("http://github.com/", "https://raw.githubusercontent.com/")
        parts = raw_url.split('/')
        raw_url = '/'.join(parts[:5]) + '/main/'.join(parts[5:])
        if path=="/":
            return requests.post(f"{raw_url}/index.html")
        else:
            return requests.post(f"{raw_url}{path}")
    else:
        return requests.post(f"{bussip}{path}", kwards)
