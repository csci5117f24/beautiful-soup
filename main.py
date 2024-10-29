from bs4 import BeautifulSoup
import requests

# Base URL for Craigslist apartment search
url = "https://minneapolis.craigslist.org/search/apa"


def fetch_listing(page_num, seen_links):
    """Fetch and parse a page of listings."""
    params = {"s": page_num * 120}  # Craigslist pagination parameter
    response = requests.get(url, params=params)

    listings = []  # Initialize a list to collect listings on this page

    if response.status_code == 200:
        print(f"Processing page {page_num}...")
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', class_='cl-static-search-result')

        for idx, result in enumerate(results, start=1):
            try:
                print(f"Processing item {idx} on page {page_num}...")

                # Extract title, price, and location
                title = result.find("div", class_="title").text.strip()
                price = result.find("div", class_="price").text.strip().replace('$', '').replace(',', '')
                location = result.find("div", class_="location").text.strip()
                link = result.find("a", href=True)['href']

                # Check if listing link is unique
                if link not in seen_links:
                    seen_links.add(link)  # Add the link to seen_links set
                    listings.append({
                        "title": title,
                        "price": int(price) if price.isdigit() else None,
                        "location": location,
                        "link": link
                    })
                    print(f"Added listing: {title}")
            except AttributeError:
                # Skip any listings missing required fields
                continue

    return listings


if __name__ == '__main__':
    all_listings = []
    seen_links = set()  # Track unique listing links

    # Loop through the first 50 pages of results
    for page in range(50):  # Adjust range as needed for more pages
        listings = fetch_listing(page, seen_links)
        if listings:
            all_listings.extend(listings)
        else:
            break

    # Define min and max price range for filtering
    min_price = 500
    max_price = 2500

    # Process and filter the listings
    for listing in all_listings:
        price = listing['price']

        # Check if the price is within the specified range
        if price is not None and min_price <= price <= max_price:
            # Print or process the filtered listing data as needed
            print(f"Title: {listing['title']}")
            print(f"Price: ${listing['price']}")
            print(f"Location: {listing['location']}")
            print(f"Link: {listing['link']}")
            print()  # For spacing between listings in output
