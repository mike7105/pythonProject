import xml.etree.ElementTree as ET

# Парсинг исходного XML
input_xml = ET.parse("input.xml")
root = input_xml.getroot()

# Создание MDD-структуры
mdd_root = ET.Element("Survey", xmlns="http://www.spss.com/ss/xml/study_mdd")
variables = ET.SubElement(mdd_root, "Variables")

for question in root.findall("question"):
    var = ET.SubElement(variables, "Variable",
                        name=question.get("id"),
                        type="numeric",
                        label=question.find("text").text)
    ET.SubElement(var, "Range",
                  min=question.get("min"),
                  max=question.get("max"))

# Сохранение MDD
tree = ET.ElementTree(mdd_root)
tree.write("output.mdd", encoding="UTF-8", xml_declaration=True)