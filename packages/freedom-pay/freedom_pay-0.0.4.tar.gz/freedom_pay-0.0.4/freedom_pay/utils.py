import random
import string
import xml.etree.ElementTree as ET
import json


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def xml_to_dict(element):
    """
    Рекурсивно преобразует XML-элемент и его подэлементы в словарь.

    :param element: XML-элемент.
    :return: Словарь, представляющий XML.
    """
    if len(element) == 0:
        return element.text

    result = {}
    for child in element:
        child_dict = xml_to_dict(child)

        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_dict)
        else:
            result[child.tag] = child_dict

    if element.attrib:
        result['_attributes'] = element.attrib

    return result


def xml_to_json(xml_string):
    """
    Преобразует XML-строку в JSON-строку.

    :param xml_string: Строка в формате XML.
    :return: Строка в формате JSON.
    """
    root = ET.fromstring(xml_string)
    xml_dict = xml_to_dict(root)
    return json.dumps(xml_dict, ensure_ascii=False, indent=2)
