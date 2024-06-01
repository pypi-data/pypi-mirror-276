import argparse
from subspy.subdomain import test_subdomains, get_default_subdomains, is_subdomain_available

VERSION = "2.2.2"
AUTHOR_INFO = "Author: Fidal, Contact : https://mrfidal.in/contact"

def save_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)
    print(f"[+] Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Subdomain enumeration tool")
    parser.add_argument("--url", help="The base URL to test subdomains against (e.g., https://example.com)")
    parser.add_argument("--sub-list", help="The file containing the list of subdomains to test")
    parser.add_argument("--save", help="Save the output to a file")
    parser.add_argument("--version", action="store_true", help="Show the version of the tool")
    parser.add_argument("--author", action="store_true", help="Show the author information")

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
    subdomain_file = args.sub_list

    if subdomain_file:
        with open(subdomain_file, "r") as lists:
            subdomains = [line.strip() for line in lists.readlines() if line.strip()]
    else:
        subdomains = get_default_subdomains()

    if is_subdomain_available(url):
        found_subdomains = test_subdomains(url, subdomains)
        output = "[+] Found subdomains :\n"
        if not found_subdomains:
            output += "[+] No subdomains found\n"
        else:
            base_url = url.split('://')[1].rstrip('/')  
            for subdomain in found_subdomains:
                output += f"Subdomain : https://{subdomain}.{base_url}\n"
        print(output.strip())

        if args.save:
            save_to_file(args.save, output.strip())
    else:
        print("[+] URL not found :", url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[+] Program interrupted by user.")
