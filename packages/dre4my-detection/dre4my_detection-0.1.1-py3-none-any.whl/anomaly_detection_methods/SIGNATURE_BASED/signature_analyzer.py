from typing import List, Dict
from utils import load_signatures, match_signature, parse_http_packet

class SignatureBasedAnalyzer:
    def __init__(self, signature_file: str = 'signatures.json'):
        """
        Инициализирует анализатор на основе сигнатур.

        :param signature_file: Путь к файлу с сигнатурами.
        """
        self.signatures = load_signatures(signature_file)

    def analyze_packet(self, packet: str) -> Dict[str, str]:
        """
        Анализирует HTTP пакет и возвращает результат анализа.

        :param packet: HTTP пакет в виде строки.
        :return: Результат анализа в виде словаря.
        """
        http_data = parse_http_packet(packet)
        classification = match_signature(http_data, self.signatures)
        http_data['classification'] = classification
        return http_data

    def analyze_traffic(self, traffic: List[str]) -> List[Dict[str, str]]:
        """
        Анализирует список HTTP пакетов.

        :param traffic: Список HTTP пакетов в виде строк.
        :return: Список результатов анализа для каждого пакета.
        """
        results = []
        for packet in traffic:
            result = self.analyze_packet(packet)
            results.append(result)
        return results

# # Пример использования
# if __name__ == "__main__":
#     analyzer = SignatureBasedAnalyzer()
#     packet = ("GET /index.html HTTP/1.1\r\n"
#               "Host: www.example.com\r\n"
#               "User-Agent: curl/7.64.1\r\n"
#               "Accept: */*\r\n"
#               "Connection: keep-alive\r\n\r\n")
#     result = analyzer.analyze_packet(packet)
#     print(result)
