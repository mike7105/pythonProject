import re
import json


def convert_to_json(input_text):
    # Извлекаем содержимое между внешними фигурными скобками
    start = input_text.find('{') + 1
    end = input_text.rfind('}')
    content = input_text[start:end].strip()

    # Регулярные выражения для парсинга
    group_pattern = re.compile(r'(\w+)\s+"([^"]+)"\s*{([^}]*)}', re.DOTALL)
    brand_pattern = re.compile(r'_(\w+)\s+"([^"]+)"\s*\[\s*value\s*=\s*(\d+)\s*\]', re.DOTALL)

    result = {"brands": {}}

    # Разбиваем на группы
    groups = re.split(r'(?<=})\s*,?\s*', content)
    for group in groups:
        if not group.strip():
            continue

        # Парсим группу
        group_match = group_pattern.search(group)
        if group_match:
            group_id, group_name, brands_content = group_match.groups()
            brands_dict = {}

            # Парсим бренды
            brands = re.findall(brand_pattern, brands_content)
            for brand_id, brand_name, value in brands:
                brands_dict[f'_{brand_id}'] = {
                    "name": brand_name,
                    "value": int(value)
                }

            result["brands"][group_id] = {
                "name": group_name,
                "brands": brands_dict
            }

    return json.dumps(result, ensure_ascii=False, indent=2)


# Пример использования
input_data = '''
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
'''

print(convert_to_json(input_data))