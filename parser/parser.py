import re
import csv
import requests
from bs4 import BeautifulSoup
import string
import time

url = "https://phl.upr.edu/hwc/data"

response = requests.get(url)
data = response.text
data = data.replace("&#39;", "'")

pattern = r'\{ v:&quot;\s*\d+&quot;,f:&quot;&lt;a href=\'(.*?)\' target=\'_blank\'&gt;(.*? [A-Za-z])&lt;/a&gt;&quot;,p: {style: \'text-align: left\'}\},\s*{ v:&quot;\s*\d+&quot;,f:&quot;(.*?)&quot;,p: {style: \'text-align: left\'}\},\s*{ v:&quot;\s*\d+&quot;,f:&quot;(.*?)&quot;,p: {style: \'text-align: left\'}\},.*?\{ v:\d+,f:&quot;([^&]*)&quot;,p: {style: \'text-align: center\'}\}]'

matches = re.findall(pattern, data)

column_titles = [
    "Название планеты", "Тип планеты",
    "Метод детектирования", "ESI"
]

planet_data = []

def planet_name_to_id(planet_name):
    translation_table = str.maketrans(string.punctuation + ' ', '-' * (len(string.punctuation) + 1))
    return planet_name.translate(translation_table).strip()


count = 1
for match in matches:
    print(f"Planet number: {count}")
    if count % 10 == 0:
        time.sleep(5)
    link, planet_name, planet_type, detection_method, esi = match
    planet_name = planet_name.strip()
    planet_id = planet_name_to_id(planet_name)

    try:
        planet_page_response = requests.get(link, timeout=10)
        planet_page_response.raise_for_status()
        planet_page_html = planet_page_response.text

        soup = BeautifulSoup(planet_page_html, 'html.parser')

        planet_sections = soup.findAll('div', class_='collapsible_section')

        target_section = None
        for section in planet_sections:
            section_id = section.get('id')
            if section_id and section_id == planet_id:
                target_section = section
                break

        if target_section:
            table = target_section.find('table')
            if table:
                rows = table.find_all('tr')
                data_row = [planet_name, planet_type, detection_method, esi]

                header_index = {}

                for row in rows:
                    header = row.find('th')
                    if header:
                        tooltip_div = header.find('div', class_='tooltip_wrapper')
                        if tooltip_div:
                            header_title = tooltip_div['title']

                            cells = row.find_all('td')
                            min_data_index = float('inf')
                            best_value_text = None

                            for cell in cells:
                                data_index = cell.get('data-index')
                                cell_text = cell.get_text(strip=True)

                                if data_index is not None and cell_text != "---":
                                    current_index = int(data_index)
                                    if current_index < min_data_index:
                                        min_data_index = current_index

                                        match = re.search(r'([-+]?\d*\.?\d+)', cell_text)
                                        if match:
                                            best_value_text = match.group(0)
                                        else:
                                            best_value_text = None

                            print(f"Заголовок: {header_title}, Значение: {best_value_text}")
                            header_index[header_title] = best_value_text if best_value_text is not None else ""

                for title in header_index:
                    if title not in column_titles:
                        column_titles.append(title)

                    index = column_titles.index(title)

                    while len(data_row) <= index:
                        data_row.append("")

                    data_row[index] = header_index[title]

                while len(data_row) < len(column_titles):
                    data_row.append("")

                print(f"Обработанная строка: {data_row}")

                planet_data.append(data_row)
    except requests.exceptions.Timeout:
        print(f"Запрос к {link} занял слишком много времени. Пропускаем эту планету.")
    except requests.exceptions.ConnectionError as e:
        print(f"Ошибка соединения: {e}. Пропускаем эту планету.")
    except requests.exceptions.RequestException as e:
        print(f"Общая ошибка запроса: {e}. Пропускаем эту планету.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}. Пропускаем эту планету.")

    count += 1
    time.sleep(1)

with open('../lab-2/planet_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(column_titles)

    for row in planet_data:
        csv_writer.writerow(row)

