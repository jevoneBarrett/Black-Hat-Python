domain_list = open("bug-bounty-domains.txt", "r")
word_list = open("bug-bounty-wordlist.txt", "w")
for domain in domain_list.readlines():
    split_domain = domain.split(".")
    if len(split_domain) > 1:
        if len(split_domain[-2]) > 2:
            word_list.write(split_domain[-2] + "\n")