import requests
import csv
from bs4 import BeautifulSoup

def get_product_data(url):
    headers = {
        "User-Agent": ""
    }
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    # Extract the product data
    title_element = soup.find("span", id="productTitle")
    title = title_element.get_text(strip=True) if title_element else "Title not available"

    price_element = soup.find("span", class_="a-offscreen")
    price = price_element.get_text(strip=True) if price_element else "Price not available"

    rating_element = soup.find("span", class_="a-icon-alt")
    rating = rating_element.get_text(strip=True) if rating_element else "Rating not available"

    description_element = soup.find("div", id="productDescription")
    description = description_element.get_text(strip=True) if description_element else "Description not available"

    review_elements = soup.find_all("span", {"data-hook": "review-body"})
    reviews = [review.get_text(strip=True) for review in review_elements]

    return [title, price, rating, description, reviews]

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Rating", "Description", "Reviews"])
        writer.writerows(data)

def scrape_amazon(keyword, num_products):
    base_url = "https://www.amazon.in"
    search_url = f"{base_url}/s?k={keyword}"
    headers = {
        "User-Agent": ""
    }

    data = []
    product_count = 0
    page = 1

    while product_count < num_products:
        url = f"{search_url}&page={page}"
        response = requests.get(url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        product_links = []
        results = soup.find_all("a", class_="a-link-normal")
        for result in results:
            link = result.get("href")
            if link and "/dp/" in link:
                product_links.append(base_url + link)

        for link in product_links:
            product_data = get_product_data(link)
            data.append(product_data)
            product_count += 1
            if product_count >= num_products:
                break

        page += 1

    return data

keyword = input("Enter a keyword: ")
num_products = 50
data = scrape_amazon(keyword, num_products)
save_to_csv(data, "amazon_products.csv")
print("Data saved to amazon_products.csv")
