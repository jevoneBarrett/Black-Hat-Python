site_list = open("bug-bounty-sites.txt", "r")
sites = site_list.readlines()
domain_list = open("bug-bounty-domains.txt", "w")
for site in sites:
    if not 'mailto' in site:
        split_site = site.split('/')
        if len(split_site) > 1:
            domain_list.write(split_site[2] + '\n')