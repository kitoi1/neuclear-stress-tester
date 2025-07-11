import requests

def check_server_health(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code != 200:
            print(f"\033[31m[!] Server responded with {response.status_code}. Cooling down...\033[0m")
            return False
        print("\033[32m[✓] Server is responsive. Proceeding...\033[0m")
        return True
    except requests.RequestException:
        print("\033[31m[!] Server not reachable. Cooling down...\033[0m")
        return False

