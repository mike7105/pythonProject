import json
import re

# Исходная структура данных
raw_data = """
listBrands "brands" define
{
gr1 "Группа 1"
{
_1 "Бренд 1"
[
value = 1
],
_2 "Бренд 2"
[
value = 2
],
_3 "Бренд 3"
[
value = 3
],
_4 "Бренд 4"
[
value = 4
]
},
gr2 "Группа 2"
{
_5 "Бренд 5"
[
value = 5
],
_34 "Бренд 34"
[
value = 34
],
_35 "Бренд 35"
[
value = 35
]
},
gr3 "Группа 3"
{
_36 "Бренд 36"
[
value = 36
],
_37 "Бренд 37"
[
value = 37
]
}
};
"""


def parse_raw_data(raw_data):
    # Регулярные выражения для парсинга
    group_pattern = re.compile(r'(\w+)\s+"([^"]+)"\s*\{')  # Группа (например, gr1 "Группа 1")
    brand_pattern = re.compile(
        r'(_\d+)\s+"([^"]+)"\s*\[\s*value\s*=\s*(\d+)\s*\]')  # Бренд (например, _1 "Бренд 1" [value = 1])

    data = {"listBrands": {"brands": {}}}
    current_group = None

    # Разделяем данные на строки
    lines = raw_data.splitlines()

    for line in lines:
        line = line.strip()

        # Ищем группу
        group_match = group_pattern.match(line)
        if group_match:
            group_id, group_name = group_match.groups()
            current_group = group_id
            data["listBrands"]["brands"][group_id] = {
                "name": group_name,
                "brands": {}
            }
            continue

        # Ищем бренд
        brand_match = brand_pattern.match(line)
        if brand_match and current_group:
            brand_id, brand_name, brand_value = brand_match.groups()
            data["listBrands"]["brands"][current_group]["brands"][brand_id] = {
                "name": brand_name,
                "value": int(brand_value)
            }

    return data


# Парсим данные
parsed_data = parse_raw_data(raw_data)

# Преобразуем в JSON
json_data = json.dumps(parsed_data, ensure_ascii=False, indent=4)

# Вывод JSON
print(json_data)
