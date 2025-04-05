import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time, random
from tqdm import tqdm


def process_product(url):
    q = {'лево': 'L', 'право': 'R', 'перед': 'F', 'зад': 'R', '': ' ', '-': ' ',
         'бывший в употреблении (контрактный)': 'Б/У',
         'новый': 'новая'}
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")
            product_data = {}

            # Извлекаем данные из таблицы
            table = soup.find('div', class_='description')
            # print(table.text)
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        key = cells[0].get_text(strip=True).replace(':', '')
                        value = cells[1].get_text(strip=True)
                        if 'Год' in value:
                            product_data[key] = value[9:]
                        else:
                            product_data[key] = value

            # Извлекаем цену
            price = soup.find("div", class_="price")
            if price:
                product_data['Цена'] = int(''.join([x for x in price.get_text(strip=True) if x.isdigit()]))
                if product_data['Цена'] < 750:
                    product_data['Цена'] = round(product_data['Цена'] * 2, -1)
                elif product_data['Цена'] < 1500:
                    product_data['Цена'] = round(product_data['Цена'] * 1.7, -1)
                elif product_data['Цена'] < 3000:
                    product_data['Цена'] = round(product_data['Цена'] * 1.5, -1)
                elif product_data['Цена'] < 6000:
                    product_data['Цена'] = round(product_data['Цена'] * 1.4, -1)
                elif product_data['Цена'] < 10000:
                    product_data['Цена'] = round(product_data['Цена'] * 1.3, -1)
                else:
                    product_data['Цена'] = round(product_data['Цена'] * 1.3, -1)

            gallery_images = soup.select('div.gallery div.image[data-src]')

            # Извлеките ссылки, начинающиеся с нужного пути
            image_urls = [
                img['data-src']
                for img in gallery_images
                if img['data-src'].startswith('https://static.tz25.ru/images/')
            ]
            product_data['Фото'] = ', '.join(image_urls)
            product_data['Запчасть'] = product_data['Название запчасти']

            product_data['F_R'], product_data['R_L'] = product_data['Расположение'].split(',', maxsplit=1)
            product_data['R_L'] = ''.join([x for x in product_data['R_L'] if 1071 < ord(x) < 1104])
            product_data['F_R'], product_data['R_L'] = q[product_data['F_R']], q[product_data['R_L']]
            product_data['Розница'] = product_data['Цена']
            product_data['Количество'] = 1
            product_data['Код'] = product_data['Код товара']
            product_data['БУ/Новая'] = q[product_data['Состояние']]

            del  product_data['Расположение'], product_data['Состояние'], product_data[
                'Название запчасти'], product_data['Код товара'], product_data['Цена']
            return product_data





    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        with open('err.txt', 'a') as err:
            print(f'{url}', file=err)
        return None


def get_product_urls(base_url, start_page, end_page):
    urls = []
    for page in tqdm(range(start_page, end_page + 1)):
        url = f"{base_url}={page}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("div", class_="head")
            for item in items:
                link = item.find('a', href=True)
                if link and 'd/' in link['href']:
                    urls.append(f"https://tz25.ru{link['href']}")
    return urls


def main():
    start_time = time.time()
    base_url = 'https://tz25.ru/catalog/?PAGEN_1'
    start_page = 1
    end_page = 1413

    # Получаем все ссылки на товары
    print("Сбор ссылок на товары...")
    product_urls = get_product_urls(base_url, start_page, end_page)

    # Обрабатываем все товары с помощью потоков
    print("Обработка товаров...")
    data = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process_product, url) for url in product_urls]
        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()
            if result:
                data.append(result)

    # Сохраняем в Excel
    df = pd.DataFrame(data)
    df.to_excel(f"tz{random.randint(1100)}.xlsx", index=False)

    print(f"Время выполнения: {round((time.time() - start_time) / 60, 2)} минут")


if __name__ == "__main__":
    main()
