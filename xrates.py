from bs4 import BeautifulSoup
import requests

url = "https://www.x-rates.com/table/?from=USD&amount=1"

result = requests.get(url).text
soup = BeautifulSoup(result, "html.parser")

# get all the text from the page
print(soup.get_text())

# get the table
tbody = soup.tbody
print(tbody)

# get the next sibling
trs = tbody.contents
print(trs[0].next_sibling)

# get the previous sibling
print(trs[2].previous_sibling)

# get the parent element
print(trs[2].parent)