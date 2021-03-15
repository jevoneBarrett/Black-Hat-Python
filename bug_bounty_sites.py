from bs4 import BeautifulSoup as bs
import requests


# Grabs all bug bounty sites

url = "https://www.vulnerability-lab.com/list-of-bug-bounty-programs.php"
r = requests.get(url)
soup = bs(r.content, 'html.parser')
tables = soup.find_all('table')
a_tags = tables[4].find_all('a')
sites_list = open("bug-bounty-sites.txt", "w")
for a in a_tags:
    sites_list.write(a.get('href') + '\n')