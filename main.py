import argparse
import re
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def parse_range(s, default_lower, default_upper):
    if not s:
        return (default_lower, default_upper)
    if '-' not in s:
        try:
            lower = float(s)
            return (lower, default_upper)
        except:
            return (default_lower, default_upper)
    parts = s.split('-', 1)
    lower_str, upper_str = parts[0].strip(), parts[1].strip()
    lower = float(lower_str) if lower_str != "" else default_lower
    upper = float(upper_str) if upper_str != "" else default_upper
    return (lower, upper)

parser = argparse.ArgumentParser(description='Yaniyo ürün kontrolü')
parser.add_argument('--discount_range', type=str, default="", help='İndirim aralığı örn: "10-50", "10-", "-20"')
parser.add_argument('--price_range', type=str, default="", help='Ürün fiyatı aralığı örn: "400-2400", "400-", "-2000"')
parser.add_argument('--interval', type=int, default=60, help='Sayfa kontrolü arasındaki bekleme süresi (saniye cinsinden)')
parser.add_argument('--url', type=str, default="tum-firsatlar", help='Kontrol edilecek URL')
args = parser.parse_args()

url = f"https://yaniyo.com/{args.url}"

discount_lower, discount_upper = parse_range(args.discount_range, 0, float('inf'))
price_lower, price_upper = parse_range(args.price_range, 0, float('inf'))
interval = args.interval

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

seen_products = set()

def extract_discount(product_element):
    try:
        discount_elem = product_element.find_element(By.CSS_SELECTOR, ".Product_badge_discount___Lm2w")
        discount_text = discount_elem.text
        match = re.search(r'\d+', discount_text)
        if match:
            return float(match.group())
    except Exception:
        return None
    return None

def extract_price(product_element):
    try:
        price_elem = product_element.find_element(By.CSS_SELECTOR, ".Product_currentPrice__qWLbH")
        price_text = price_elem.text
        price_clean = price_text.replace("₺", "").strip().replace(",", ".")
        return float(price_clean)
    except Exception:
        return None
    return None

def extract_product_link(product_element):
    try:
        a_elem = product_element.find_element(By.TAG_NAME, "a")
        return a_elem.get_attribute("href")
    except Exception:
        return None

try:
    driver.get(url)
    time.sleep(5)
    
    if "404" in driver.title:
        print(f"Hata: Sayfa bulunamadı! ({url})")
        driver.quit()
        exit()
    
    initial_products = driver.find_elements(By.CSS_SELECTOR, ".Product_product__bI6Qj")
    for product in initial_products:
        link = extract_product_link(product)
        if link:
            seen_products.add(link)
    print("İlk yüklemede bulunan ürünler göz ardı edildi.")
    
    try:
        while True:
            driver.get(url)
            time.sleep(5)
            product_elements = driver.find_elements(By.CSS_SELECTOR, ".Product_product__bI6Qj")
            
            for product in product_elements:
                link = extract_product_link(product)
                if not link or link in seen_products:
                    continue
                
                discount = extract_discount(product)
                price = extract_price(product)
                if discount is None:
                    discount = 0
                
                if (discount >= discount_lower and discount <= discount_upper and 
                    price is not None and price >= price_lower and price <= price_upper):
                    seen_products.add(link)
                    print(f"Yeni ürün bulundu: {link} | İndirim: {discount}% | Fiyat: ₺{price}")
                    webbrowser.open(link)
            
            print(f"Kontrol tamamlandı. {interval} saniye bekleniyor...")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("Kapatma isteği alındı. Çıkılıyor...")
    
finally:
    driver.quit()
