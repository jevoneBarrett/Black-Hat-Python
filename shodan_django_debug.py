import shodan


with open("shodan_api_key.txt", "r") as f:
    SHODAN_API_KEY = f.readline()
api = shodan.Shodan(SHODAN_API_KEY)
words = open("bug-bounty-wordlist.txt", "r")
django_debug_list = open("django-debug-list.txt", "w")
for word in words.readlines():
    query = "html:'URLconf defined' ssl:" + word.strip('n')
    try:
        results = api.search(query)
        print(f"Results found: {results['total']}")
        for result in results['matches']:
            print(word)
            print(f"IP: {result['ip_str']}")
            port = result['port']
            if port in [80, 443]:
                if port == 443:
                    ip = f"https://{result['ip_str']}"
                else:
                    ip = f"http://{result['ip_str']}"
            else:
                ip = f"http://{result['ip_str']}:{port}"
            django_debug_list.write(ip + '\n')
            print('\n')
    except Exception as e:
        print(e)