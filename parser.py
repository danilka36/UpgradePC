import requests
from bs4 import BeautifulSoup
import json
import time
import random

LINKS = {
    "r5_5600": "https://example-store.ru/product/amd-ryzen-5-5600",
    "xeon": "https://example-store.ru/product/xeon-e5-2667-v3",
    "rx5700xt": "https://example-store.ru/product/radeon-rx-5700-xt",
    "rtx3060": "https://example-store.ru/product/geforce-rtx-3060"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9"
}

def parse_price(component_id, url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        print(f"Запрос к {component_id}: Код ответа сервера = {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Пытаемся найти тег с ценой. 
            # ВНИМАНИЕ: Если ты используешь реальные ссылки, проверь через F12 класс цены на сайте!
            price_tag = soup.find("span", class_="current-price")
            
            if price_tag:
                clean_price = "".join(filter(str.isdigit, price_tag.text))
                if clean_price:
                    return int(clean_price)
            else:
                print(f"Предупреждение: На странице {component_id} не найден тег с классом 'current-price'")
        else:
            print(f"Ошибка: Сайт вернул код {response.status_code} вместо 200")
    except Exception as e:
        print(f"Критическая ошибка при парсинге {component_id}: {e}")
    return None

def main():
    prices_db = {}
    
    for component_id, url in LINKS.items():
        print(f"--- Старт парсинга для: {component_id} ---")
        price = parse_price(component_id, url)
        
        if price:
            prices_db[component_id] = price
            print(f"Результат записан: {price} руб.")
        else:
            # Если цену не нашли, временно ставим 0, чтобы файл создался и мы увидели структуру
            prices_db[component_id] = 0
            print(f"Внимание: Для {component_id} установлен заглушечный ноль.")
            
        time.sleep(random.randint(1, 3))
    
    prices_db["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Файл создастся в любом случае!
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(prices_db, f, ensure_ascii=False, indent=4)
    print("Процесс завершен. Файл prices.json успешно сгенерирован на диске!")

if __name__ == "__main__":
    main()
