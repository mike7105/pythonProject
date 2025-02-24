import comtypes.client


def GetTypeFields(num: int) -> str:
    if num == 0:
        return "mtVariable"
    elif num == 1:
        return "mtGrid"
    elif num == 3:
        return "mtClass"
    else:
        return "Unknown"


def GetTypeVariables(num: int) -> str:
    if num == 0:
        return "None"
    elif num == 1:
        return "Long"
    elif num == 2:
        return "Text"
    elif num == 3:
        return "Categorical"
    elif num == 4:
        return "Object"
    elif num == 5:
        return "Date"
    elif num == 6:
        return "Double"
    elif num == 7:
        return "Boolean"
    else:
        return "Unknown"


# Подключение к объектной модели MDD
try:
    # Создание экземпляра объекта MDM Application
    mdm_app = comtypes.client.CreateObject("MDM.Document")

    # Открытие MDD-файла
    mdd_file_path = r"C:\Users\Mihail.chesnokov\Documents\GitHub\pythonProject\xmlTomdd\TestStructure.mdd" # Укажите путь к вашему MDD-файлу
    mdm_app.Open(mdd_file_path)

    # # Получение коллекции полей (Fields)
    # fields = mdm_app.Fields
    #
    # print(f"Всего полей: {fields.Count}")
    #
    # # Цикл по всем полям
    # for i in range(0, fields.Count):  # Индексация начинается с 1
    #     field = fields.Item(i)
    #     field_name = field.FullName
    #     field_type = GetTypeFields(field.ObjectTypeValue)  # Тип поля (например, текстовый, числовой и т.д.)
    #     field_label = field.Label
    #
    #     print(f"Поле {i}: \t\nИмя = {field_name}, \t\nТип = {field_type}, \t\nФормулировка = {field_label}\n")

    variables = mdm_app.Variables

    print(f"Всего Variables: {variables.Count}")

    # Цикл по всем полям
    # for i in range(0, variables.Count):  # Индексация начинается с 1
    #     field = variables.Item(i)
    for field in variables:
        field_name = field.FullName
        field_type = GetTypeVariables(field.DataType)  # Тип поля (например, текстовый, числовой и т.д.)

        if field.DataType == 3:
            field_effmax = field.EffectiveMaxValue
            field_catcount = field.Categories.Count

            categs = [f"{Categ.FullName}:{Categ.Value}:{Categ.Label}" for Categ in field.Categories]
        else:
            field_effmax = ""
            field_catcount = ""
            categs = []

        field_label = field.Label

        print(f"variable \n"
              f"\tFullName = {field_name}, \n"
              f"\tDataType = {field_type}, \n"
              f"\tEffectiveMaxValue = {field_effmax}, \n"
              f"\tCategoriesCount = {field_catcount}, \n"
              f"\ttext question = {field_label}\n"
              f"\tcategories = "
              )
        if categs:
            print('\t\t' + '\n\t\t'.join(categs))

    # Закрытие документа
    mdm_app.Close()

except Exception as e:
    print(f"Произошла ошибка: {e}")



