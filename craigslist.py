from bs4 import BeautifulSoup
import requests

url = "https://minneapolis.craigslist.org/search/apa"

response = requests.get(url)
assert response.status_code == 200

soup = BeautifulSoup(response.text, 'html.parser')

results = soup.find_all('li', class_='cl-static-search-result')

listings = []
for result in results:
    title = result.find("div", class_="title").text.strip()
    price = result.find("div", class_="price").text.strip().replace('$', '').replace(',', '')
    location = result.find("div", class_="location").text.strip()
    link = result.find("a", href=True)['href']

    listings.append({
        "title": title,
        "price": int(price) if price.isdigit() else None,
        "location": location,
        "link": link
    })

min_price = 2000
max_price = 2500
for listing in listings:
    price = listing['price']
    if price is not None and min_price <= price <= max_price:
        print(f"Title: {listing['title']}")
        print(f"Price: ${listing['price']}")
        print(f"Location: {listing['location']}")
        print(f"Link: {listing['link']}")
