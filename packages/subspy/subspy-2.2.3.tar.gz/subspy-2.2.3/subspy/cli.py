import argparse
import threading
import time
import requests
from subspy.subdomain import test_subdomains, get_default_subdomains, is_subdomain_available

VERSION = "2.2.3"
AUTHOR_INFO = "Author: Fidal, Contact : https://mrfidal.in/contact"

def save_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)
    print(f"[+] Results saved to {filename}")

def parse_time(time_str):
    unit = time_str[-1]
    value = int(time_str[:-1])
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    else:
        raise ValueError("Invalid time format. Use 's' for seconds, 'm' for minutes, or 'h' for hours.")

def check_url_validity(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def run_tool(url, subdomains, silent, save_path, stop_event, tried_count, found_count):
    output = "[+] Found subdomains:\n"
    if is_subdomain_available(url):
        found_subdomains = test_subdomains(url, subdomains, silent, stop_event, tried_count, found_count)
        if not found_subdomains:
            output += "[+] No subdomains found\n"
        else:
            base_url = url.split('://')[1].rstrip('/')  # Extract base URL without protocol
            for subdomain in found_subdomains:
                output += f"Subdomain : https://{subdomain}.{base_url}\n"
        print(output.strip())
        if save_path:
            save_to_file(save_path, output.strip())
    else:
        print("[+] URL not found :", url)

def display_counts(tried_count, found_count, stop_event):
    while not stop_event.is_set():
        print(f"\rTried : ({tried_count[0]}) Found : ({found_count[0]})", end="")
        time.sleep(1)
    print(f"\rTried : ({tried_count[0]}) Found : ({found_count[0]})")

def main():
    parser = argparse.ArgumentParser(description="Subdomain enumeration tool")
    parser.add_argument("--url", help="The base URL to test subdomains against (e.g., https://example.com)")
    parser.add_argument("--sub-list", help="The file containing the list of subdomains to test")
    parser.add_argument("--save", help="Save the output to a file")
    parser.add_argument("--version", action="store_true", help="Show the version of the tool")
    parser.add_argument("--author", action="store_true", help="Show the author information")
    parser.add_argument("--silent", action="store_true", help="Suppress output of wrong subdomains")
    parser.add_argument("--time", help="Run the tool for a specific amount of time (e.g., 5m, 50s, 1h)")

    args = parser.parse_args()

    if args.version:
        print(f"Subspy version : {VERSION}")
        return

    if args.author:
        print(AUTHOR_INFO)
        return

    if not args.url:
        parser.print_help()
        return

    url = args.url

    if not check_url_validity(url):
        print(f"[+] URL not valid or not reachable : {url}")
        return

    subdomain_file = args.sub_list

    if subdomain_file:
        with open(subdomain_file, "r") as lists:
            subdomains = [line.strip() for line in lists.readlines() if line.strip()]
    else:
        subdomains = get_default_subdomains()

    stop_event = threading.Event()
    tried_count = [0]
    found_count = [0]

    timeout = parse_time(args.time) if args.time else None

    tool_thread = threading.Thread(target=run_tool, args=(url, subdomains, args.silent, args.save, stop_event, tried_count, found_count))
    display_thread = threading.Thread(target=display_counts, args=(tried_count, found_count, stop_event))

    tool_thread.start()
    display_thread.start()

    if timeout:
        tool_thread.join(timeout)
        if tool_thread.is_alive():
            print("\n[+] Time limit reached. Stopping execution.")
            stop_event.set()
            tool_thread.join()
    else:
        tool_thread.join()

    stop_event.set()
    display_thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[+] Program interrupted by user.")
