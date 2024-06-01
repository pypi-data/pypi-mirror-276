import os
import requests

def is_subdomain_available(subdomain_url):
    try:
        r = requests.get(subdomain_url)
        r.raise_for_status()
        return True, r.status_code
    except requests.RequestException:
        return False, None

def fix_url(url):
    if url.startswith("http://"):
        return url[len("http://"):]
    elif url.startswith("https://"):
        return url[len("https://"):]
    return url

def test_subdomains(url, subdomains):
    tried_subdomains = []
    found_subdomains = []
    fixed_url = fix_url(url)
    for idx, subdomain in enumerate(subdomains, start=1):
        url_with_subdomain = f"https://{subdomain}.{fixed_url}"
        tried_subdomains.append(url_with_subdomain)
        available, status_code = is_subdomain_available(url_with_subdomain)
        if available:
            found_subdomains.append(subdomain)
            print(f"\033[97m ({idx}/{len(subdomains)}) [\033[92m+\033[97m] \033[92mSubdomain found : {subdomain}.{fixed_url} \033[97m(\033[92mStatus Code : {status_code}\033[97m)")
        else:
            print(f"\033[97m ({idx}/{len(subdomains)}) [\033[91m+\033[97m] \033[91mWrong Subdomain : {subdomain}.{fixed_url} \033[97m(\033[91mStatus Code : {status_code}\033[97m)")

    return found_subdomains

def get_default_subdomains():
    current_dir = os.path.dirname(__file__)
    default_subdomains_path = os.path.join(current_dir, "default_subdomains.txt")
    with open(default_subdomains_path, "r") as file:
        return [line.strip() for line in file if line.strip()]
