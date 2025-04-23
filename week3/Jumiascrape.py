import requests
from bs4 import BeautifulSoup
import re


headers = {"User-Agent":"Mozilla/5.0"}
all_products = []
for  page in range(1, 5):
     url = f"https://www.jumia.co.ke/mlp-maybelline-store/?page={page}"
     response = requests.get(url, headers=headers)

     if response.status_code == 200:
        print(f"\n Page {page} Request was successful")
        soup_page = BeautifulSoup(response.content, "html.parser")
        products_cards = soup_page.find_all("article", class_="prd")
        print(f"Found{len(products_cards)} products")
    
        for product in products_cards [:10]:
            brand_tag = product.find("a", class_="core")
            
            if brand_tag:  
              product_name = brand_tag.get("data-ga4-item_name" ,"NA") 
              product_brand = brand_tag.get("data-ga4-item_name" , "NA")
            else:
              product_name = "NA"
              product_brand = "NA"
                    
            price_tag = product.find("div", class_="prc")
            price_text = price_tag.text.strip() if price_tag else "0"
            price = int(re.sub(r"[^\d]", "", price_text))
    
            old_price_text = price_tag.get("data-oprc", "0") if price_tag else "0"
            old_price = int(re.sub(r"[^\d]", "", old_price_text))
            
    
            discount_tag = product.find("div",class_="bdg _dsct")
            discount_text = discount_tag.text.strip() if discount_tag else "0%"
            discount_digits = re.sub(r"[^\d]","",discount_text)
            discount = int(discount_digits) if discount_digits.isdigit() else 0
            print("Raw discount text:",discount_text)
            
            reviews_tag = product.find("div",class_="rev")
            if reviews_tag:
               reviews_match = re.search(r"\d+", reviews_tag.text)
               reviews = int(reviews_match.group()) 
            else:
                print("Reviews tag not found.")
                reviews = 0
    
            rating_tag = product.find("div", class_="stars _s")
            if rating_tag:
               rating_match = re.search(r"width:(\d+)%", str(rating_tag))
               rating = round(int(rating_match.group(1))/ 20, 1) if rating_match else 0.0
            else:
                print("Rating tag not found")
                rating = 0.0
                
            popularity_score = (rating * 20) + (reviews * 2) + discount - (price * 0.0005)
            popularity_score = round(popularity_score, 2)
                
            print(f"product: {product_name}")
            print(f"product Brand: {product_brand}")          
            print(f"product Price: KES{price}")
            print(f"product Old Price:{old_price}")
            print(f"product Discount:{discount}")
            print(f"product Rating:{rating}/5")
            print(f"product Reviews:{reviews}")
            print(f"product popularity:{round(popularity_score,2)} ") 
            print("-" * 40)  
            
            popularity_score = (reviews*rating) + (discount*0.5) - (price*0.0005)
            all_products.append({
                "name": product_name,
                "brand": product_brand,
                "price": price,
                "old_price": old_price,
                "discount": discount,
                "rating": rating,
                "reviews":reviews,
                "popularity": round(popularity_score, 2)
            })
           
            popular_products = sorted(all_products,key= lambda x: x["popularity"],reverse=True)   
            print("\n Top 5 Popular Products to recommend:")
            for prod in popular_products [:5]:
                print(f"{prod['name']} - Popularity Score:{prod['popularity']}") 
                print(f"Product price: KES{prod['price']} | discount: {prod['discount']}%")
                print(f"product Rating: {prod['rating']}/5 | Reviews: {prod['reviews']}")
                print(f"Product Popularity Score: {prod['popularity']}")
                   
if response.status_code != 200:
    print(f"Request failed: {response.status_code}")
    
    
import csv

csv_filename = "maybelline_products.csv"

headers = ["name","brand","price","old_price","discount","rating","reviews","popularity"]

with open(csv_filename,mode="w", newline="",encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_products)
    
    print(f"\n Data exported to {csv_filename}")    
