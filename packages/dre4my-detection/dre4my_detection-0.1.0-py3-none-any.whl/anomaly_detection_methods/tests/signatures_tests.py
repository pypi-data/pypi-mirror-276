import sys
import os
import pandas as pd

# Добавление пути к директории SIGNATURE_BASED
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../SIGNATURE_BASED')))

from signature_analyzer import SignatureBasedAnalyzer

def convert_row_to_http_packet(row):
    """
    Преобразует строку из DataFrame в формат HTTP-пакета.

    :param row: Строка из DataFrame.
    :return: HTTP-пакет в виде строки.
    """
    http_packet = (
        f"{row['Method']} {row['URL']} HTTP/1.1\r\n"
        f"Host: {row['host']}\r\n"
        f"User-Agent: {row['User-Agent']}\r\n"
        f"Pragma: {row['Pragma']}\r\n"
        f"Cache-Control: {row['Cache-Control']}\r\n"
        f"Accept: {row['Accept']}\r\n"
        f"Accept-Encoding: {row['Accept-encoding']}\r\n"
        f"Accept-Charset: {row['Accept-charset']}\r\n"
        f"Language: {row['language']}\r\n"
        f"Cookie: {row['cookie']}\r\n"
        f"Content-Type: {row['content-type']}\r\n"
        f"Connection: {row['connection']}\r\n"
        f"Content-Length: {row['lenght']}\r\n\r\n"
        f"{row['content']}"
    )
    return http_packet

def analyze_dataset(csv_file, signature_file):
    """
    Анализирует датасет и возвращает результаты анализа.

    :param csv_file: Путь к CSV-файлу с датасетом.
    :param signature_file: Путь к файлу с сигнатурами.
    :return: DataFrame с результатами анализа.
    """
    # Загрузка датасета
    df = pd.read_csv(csv_file, delimiter=';')

    # Инициализация анализатора
    analyzer = SignatureBasedAnalyzer(signature_file)

    # Список для хранения результатов
    results = []

    # Анализ каждой строки
    for _, row in df.iterrows():
        http_packet = convert_row_to_http_packet(row)
        analysis_result = analyzer.analyze_packet(http_packet)
        results.append(analysis_result)

    # Создание DataFrame с результатами
    results_df = pd.DataFrame(results)
    return results_df

# Пример использования
if __name__ == "__main__":
    results = analyze_dataset('/mnt/e/ITMO/anomaly_detection_methods-library/anomaly_detection_methods/tests/datasets/csic_database-no_classification.csv', 
                              '../SIGNATURE_BASED/signatures.json')
    print(results)
    # Сохранение результатов в CSV (если нужно)
    results.to_csv('/mnt/e/ITMO/anomaly_detection_methods-library/anomaly_detection_methods/tests/signatures_tests-results.csv', index=False)
