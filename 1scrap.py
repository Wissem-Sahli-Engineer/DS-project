import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

# 1. Setup Browser
chrome_options = Options()
# chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(options=chrome_options)

all_laptops = []
all_laptops2 = []  # Second method: extract from description

try:
    k = 1
    nb_pages = 1  # Start with 1 so the loop begins

    while k <= nb_pages: 
        url = f"https://www.tunisianet.com.tn/681-pc-portable-gamer?page={k}"
        print(f"--- Working: Accessing Page {k} / {nb_pages if nb_pages > 1 else '?'} ---")
        
        driver.get(url)
        time.sleep(2) # Wait for page to load

        # Update nb_pages only on the first loop
        if k == 1:
            try:
                pagination_text = driver.find_element(By.CSS_SELECTOR, "nav.pagination div.text-xs-left").text
                # Example text: "Affichage 1-24 de 296 article(s)" 
                parts = pagination_text.split()
                total_items = int(parts[3]) # Grabs 296 
                
                # To get '24' from '1-24'
                items_per_page = int(parts[1].split('-')[1]) 
                
                nb_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0)
                print(f"--- Detected: {total_items} items, {nb_pages} pages to scrape ---")
            except Exception as e:
                print("Could not calculate total pages, defaulting to 1.")

        # Find all product containers
        products = driver.find_elements(By.CLASS_NAME, "wb-product-desc") # [cite: 2]

        for product in products:
            try:
                # METHOD 1: Extracting from title (original method)
                ref = (product.find_element(By.CLASS_NAME, "product-title").text).split('/')
                
                # Handle cases where the title doesn't have all parts
                name = ref[0] if len(ref) > 0 else "N/A"
                cpu = ref[1] if len(ref) > 1 else "N/A"
                gpu = ref[2] if len(ref) > 2 else "N/A"
                ram = ref[3] if len(ref) > 3 else "N/A"
                storage = ref[4] if len(ref) > 4 else "N/A"
                color = ref[5] if len(ref) > 5 else "N/A"
                ref_code = product.find_element(By.CLASS_NAME, "product-reference").text

                desc = product.find_element(By.CLASS_NAME, "listds").text
                desc_list = desc.split("-")

                # Extract screen info from first item (split by comma and get 3rd element)
                screen = desc_list[0].split(",")[2].strip() if len(desc_list[0].split(",")) > 2 else "N/A"
                # Extract guarantee number (year) at position [10] from the last item
                garentie = desc_list[-1][10] if len(desc_list) > 0 and len(desc_list[-1]) > 10 else "N/A"

                price = product.find_element(By.CLASS_NAME, "price").get_attribute('textContent')
                availability = product.find_element(By.CSS_SELECTOR, "#stock_availability span").get_attribute('textContent')
                
                all_laptops.append({
                    "Name": name,
                    "Reference": ref_code,
                    "CPU": cpu,
                    "GPU": gpu,
                    "RAM": ram,
                    "Storage": storage,
                    "Refresh screen": screen,
                    "Color": color,
                    "Price": price,
                    "Garentie": garentie,
                    "Availability": availability,
                })
                
                # METHOD 2: Extracting from description (lines 35-53 logic)
                # Extract CPU from description
                cpu2 = "N/A"
                cpu_match = re.search(r'Processeur.*?<strong>(.*?)</strong>', desc, re.IGNORECASE)
                if not cpu_match:
                    cpu_match = re.search(r'(Intel Core [^\s,]+|AMD Ryzen [^\s,]+|i[357]-\d+\w*)', desc)
                if cpu_match:
                    cpu2 = cpu_match.group(1).strip()
                
                # Extract GPU from description
                gpu2 = "N/A"
                gpu_match = re.search(r'(?:RTX|GTX|GeForce|Radeon)\s+\d+\s*\w*', desc)
                if gpu_match:
                    gpu2 = gpu_match.group(0).strip()
                
                # Extract RAM from description 
                ram2 = "N/A"
                ram_match =re.search(r'(\d+\s*(?:Go|To))\s*(?:SSD|HDD|NVMe)?', desc)
                if ram_match:
                    ram2 = ram_match.group(1).strip()
                
                # Extract Storage from description (look for SSD/HDD/Disque pattern)
                storage2 = "N/A"
                storage_match = re.search(r'(?:Disque|SSD|HDD|NVMe).*?(\d+\s*(?:Go|To))', desc)
                if storage_match:
                    storage2 = storage_match.group(1).strip()
                
                # Extract color if available in description
                color2 = "N/A"
                color_match = re.search(r'Couleur\s+([^\-]+)', desc)
                if color_match:
                    color2 = color_match.group(1).strip()
                
                all_laptops2.append({
                    "Name": name,
                    "Reference": ref_code,
                    "CPU": cpu2,
                    "GPU": gpu2,
                    "RAM": ram2,
                    "Storage": storage2,
                    "Refresh screen": screen,
                    "Color": color2,
                    "Price": price,
                    "Garentie": garentie,
                    "Availability": availability,
                })
                
            except Exception as e:
                print(f"!!! Error: Failed to extract data from product - {str(e)} !!!")
                continue # Skip individual item if it fails
        
        k += 1 # Move to next page

    # 2. Convert to DataFrame
    df = pd.DataFrame(all_laptops)
    df2 = pd.DataFrame(all_laptops2)
    
    print(f"--- Success: Scraped {len(df)} items (Method 1) and {len(df2)} items (Method 2)! ---")
    
    # Save results
    df.to_csv("gaming_laptops.csv", index=False)
    print("Data saved to gaming_laptops.csv")
    
    df2.to_csv("gaming_laptops2.csv", index=False)
    print("Data saved to gaming_laptops2.csv (extracted from descriptions)")

except Exception as e:
    print(f"!!! Critical Error: {e} !!!")

finally:
    driver.quit()

print("\n--- Method 1 (Title Split) ---")
print(df.head())
print("\n--- Method 2 (Description Parsing) ---")
print(df2.head())