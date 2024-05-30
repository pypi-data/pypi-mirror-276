import os
import joblib
import pandas as pd

# Определение пути к файлам модели и векторизатора
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'logistic_regression_model.pkl')
vectorizer_path = os.path.join(current_dir, 'tfidf_vectorizer.pkl')

# Загрузка модели и векторизатора
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# Функция для анализа нового HTTP-пакета
def analyze_http_packet(http_packet):
    # Подготовка данных пакета
    packet_data = pd.DataFrame([http_packet])
    packet_data['content'].fillna('', inplace=True)
    packet_data['text'] = (packet_data['Method'] + ' ' + packet_data['content-type'].fillna('') + ' ' + 
                           packet_data['connection'] + ' ' + packet_data['content'] + ' ' + packet_data['URL'])
    
    # Преобразование текстовых данных с использованием TF-IDF
    packet_tfidf = vectorizer.transform(packet_data['text'])
    
    # Предсказание модели
    prediction = model.predict(packet_tfidf)
    
    # Возвращение результата
    return 'Anomalous' if prediction[0] == 1 else 'Normal'

# Пример использования функции
if __name__ == '__main__':
    # Пример нового HTTP-пакета для анализа
    new_http_packet = {
        'Method': 'POST',
        'content-type': 'application/x-www-form-urlencoded',
        'connection': 'close',
        'lenght': '68',
        'content': 'id=3&nombre=Vino+Rioja&precio=100&cantidad=55&bodega=La+Rioja',
        'URL': 'http://localhost:8080/tienda1/publico/anadir.jsp HTTP/1.1'
    }
    
    # Анализ пакета
    result = analyze_http_packet(new_http_packet)
    print(f'The HTTP packet is classified as: {result}')
