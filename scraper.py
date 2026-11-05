import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import re
import os

DB_PATH = "scraped_data.db"

def scrape_catalog(num_pages=3):
    """
    Scrapes product catalog across multiple pages, handles pagination,
    extracts structured fields, cleans pricing/ratings, and persists to SQLite.
    """
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    
    records = []
    
    for page in range(1, num_pages + 1):
        target_url = base_url.format(page)
        try:
            response = requests.get(target_url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, "lxml")
            articles = soup.find_all("article", class_="product_pod")
            
            for article in articles:
                # Title
                title_tag = article.h3.find("a")
                title = title_tag.get("title", title_tag.text).strip()
                
                # Price extraction & cleaning
                price_text = article.find("p", class_="price_color").text
                price_match = re.search(r"[\d\.]+", price_text)
                price = float(price_match.group(0)) if price_match else 0.0
                
                # Rating extraction
                rating_class = article.find("p", class_="star-rating").get("class", [])
                rating = 0
                for r_name, r_val in rating_map.items():
                    if r_name in rating_class:
                        rating = r_val
                        break
                        
                # Availability
                avail_tag = article.find("p", class_="instock availability")
                availability = "In Stock" if avail_tag and "In stock" in avail_tag.text else "Out of Stock"
                
                records.append({
                    "Title": title,
                    "Price_GBP": price,
                    "Rating": rating,
                    "Availability": availability,
                    "Page": page
                })
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            
    df = pd.DataFrame(records)
    
    # Save to SQLite
    if not df.empty:
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("products", conn, if_exists="replace", index=False)
        conn.close()
        
    return df

def get_persisted_data():
    """Retrieves cached data from SQLite if available."""
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql("SELECT * FROM products", conn)
            conn.close()
            return df
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()
