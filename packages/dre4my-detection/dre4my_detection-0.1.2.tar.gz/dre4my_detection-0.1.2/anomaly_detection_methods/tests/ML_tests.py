import os
import joblib
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

# Определение пути к файлам модели, векторизатора и датасета
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '..', 'ML_BASED', 'logistic_regression_model.pkl')
vectorizer_path = os.path.join(current_dir, '..', 'ML_BASED', 'tfidf_vectorizer.pkl')
dataset_path = os.path.join(current_dir, 'datasets', 'csic_database-no_classification.csv')

# Загрузка модели и векторизатора
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# Загрузка датасета
df = pd.read_csv(dataset_path, delimiter=';')

# Удаление неинформативных колонок
df = df.drop(columns=['User-Agent', 'Pragma', 'Cache-Control', 'Accept', 'Accept-encoding', 'Accept-charset', 'language', 'host', 'cookie'])

# Заполнение пропущенных значений в текстовых полях пустыми строками
df['content'].fillna('', inplace=True)

# Создание нового столбца с текстовыми данными для анализа
df['text'] = df['Method'] + ' ' + df['content-type'].fillna('') + ' ' + df['connection'] + ' ' + df['content'] + ' ' + df['URL']

# Преобразование текстовых данных с использованием TF-IDF
X_tfidf = vectorizer.transform(df['text'])

# Предсказания на данных
predictions = model.predict(X_tfidf)

# Добавление предсказаний в датасет
df['predictions'] = predictions

# # Вывод первых 5 строк с предсказаниями
# print(df[['Method', 'content-type', 'connection', 'lenght', 'content', 'URL', 'predictions']].head())

# Сохранение результатов в новый CSV-файл
output_path = os.path.join(current_dir, 'ML_tests-results.csv')
df.to_csv(output_path, index=False)

print(f'Results saved to {output_path}')
