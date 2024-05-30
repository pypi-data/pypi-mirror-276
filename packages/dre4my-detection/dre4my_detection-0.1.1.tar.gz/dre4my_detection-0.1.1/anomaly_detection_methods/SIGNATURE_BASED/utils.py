import json
import re
import os
from typing import List, Dict

def load_signatures(file_path: str) -> Dict[str, List[str]]:
    """
    Загружает сигнатуры из JSON файла.

    :param file_path: Путь к файлу с сигнатурами.
    :return: Словарь сигнатур.
    """
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, file_path)
    
    with open(full_path, 'r') as file:
        data = json.load(file)
    return data["vulnerabilities"]

def match_signature(http_data: Dict[str, str], signatures: Dict[str, List[str]]) -> str:
    """
    Сравнивает HTTP данные с сигнатурами и возвращает метку найденной сигнатуры.

    :param http_data: HTTP данные.
    :param signatures: Словарь сигнатур.
    :return: Метка найденной сигнатуры или 'benign', если совпадений нет.
    """
    for vulnerability, patterns in signatures.items():
        for pattern in patterns:
            if re.search(pattern, str(http_data)):
                return vulnerability
    return 'benign'

def parse_http_packet(packet: str) -> Dict[str, str]:
    """
    Парсит HTTP пакет и возвращает словарь с HTTP данными.

    :param packet: HTTP пакет в виде строки.
    :return: Словарь с HTTP данными.
    """
    http_data = {}
    lines = packet.split('\r\n')
    request_line = lines[0].split(' ')
    http_data['Method'] = request_line[0]
    http_data['URL'] = request_line[1]
    
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            http_data[key.lower()] = value
        elif line == '':
            break

    # Остальное содержимое пакета
    content_index = packet.index('\r\n\r\n') + 4
    http_data['content'] = packet[content_index:]
    http_data['length'] = str(len(http_data['content']))

    return http_data