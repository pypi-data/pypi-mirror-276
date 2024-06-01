import argparse
from subdomain_tool.banner import print_banner
from subdomain_tool.subdomain import test_subdomains, get_default_subdomains, is_subdomain_available

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Subdomain enumeration tool")
    parser.add_argument("--url", required=True, help="The base URL to test subdomains against (e.g., https://example.com)")
    parser.add_argument("--sub-list", help="The file containing the list of subdomains to test")

    args = parser.parse_args()

    url = args.url
    subdomain_file = args.sub_list

    if subdomain_file:
        with open(subdomain_file, "r") as lists:
            subdomains = [line.strip() for line in lists.readlines() if line.strip()]
    else:
        subdomains = get_default_subdomains()

    if is_subdomain_available(url):
        found_subdomains = test_subdomains(url, subdomains)
        if not found_subdomains:
            print(f"\033[97m [\033[91m+\033[97m] \033[91mNo subdomains found")
        else:
            print(f"\033[97m [\033[92m+\033[97m] \033[92mFound subdomains : ")
            for subdomain in found_subdomains:
                print(subdomain)
    else:
        print(f"\033[97m [\033[91m+\033[97m] \033[91mURL not found : ", url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\033[97m [\033[91m+\\033[97m] \033[91mProgram interrupted by user.")
