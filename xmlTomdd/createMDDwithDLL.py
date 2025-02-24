import comtypes.client

try:
    # Создание экземпляра объекта MDM Application
    mdm_app = comtypes.client.CreateObject("MDM.Document")
    # Создание нового документа
    # mdm_doc = mdm_app.NewDocument()

    mdd_file_path = r"C:\Users\Mihail.chesnokov\Documents\GitHub\pythonProject\xmlTomdd\TestStructure.mdd"  # Укажите путь к вашему MDD-файлу
    mdm_app.Open(mdd_file_path)

    # Добавление переменной (вопроса)
    question_name = "Gender"
    question_text = "Какой ваш пол?"
    obj = mdm_app.CreateObject("Gender", "Пол", 7)
    mdm_app.Fields.Add(obj)  # 1 - тип поля (текстовый)
    # MDM.Fields.Add(MDM.CreateObject("Gender", "ïîë", mtField))

    # Получение созданного поля
    field = mdm_app.Fields.Item(1)
    field.Label = question_text  # Установка текста вопроса

    # Добавление вариантов ответа
    field.Categories.Add("_1", "Мужской")
    field.Categories.Add("_2", "Женский")

    # Сохранение MDD-файла
    output_path = r"C:\Users\Mihail.chesnokov\Documents\GitHub\pythonProject\xmlTomdd\output_file.mdd"  # Укажите путь для сохранения
    mdm_doc.SaveAs(output_path)

    print(f"MDD-файл успешно создан: {output_path}")

    # Закрытие документа
    mdm_doc.Close()

except Exception as e:
    print(f"Произошла ошибка: {e}")
