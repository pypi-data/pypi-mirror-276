import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Определение пути к файлу с данными и загрузка датасета
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'tests', 'datasets', 'csic_database.csv')
df = pd.read_csv(data_path, delimiter=';')

# Удаление неинформативных колонок
df = df.drop(columns=['User-Agent','Pragma', 'Cache-Control', 'Accept', 'Accept-encoding', 'Accept-charset', 'language', 'host', 'cookie'])

# Заполнение пропущенных значений в текстовых полях пустыми строками
df['content'].fillna('', inplace=True)

# Создание нового столбца с текстовыми данными для анализа
df['text'] = df['Method'] + ' ' + df['content-type'].fillna('') + ' ' + df['connection'] + ' ' + df['content'] + ' ' + df['URL']

# Определение целевой переменной
y = df['classification']

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.2, random_state=42)

# Преобразование текстовых данных с использованием TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # Ограничение числа признаков для производительности
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Обучение модели логистической регрессии
log_reg = LogisticRegression()
log_reg.fit(X_train_tfidf, y_train)

# Предсказания на тестовых данных
y_pred = log_reg.predict(X_test_tfidf)

# Оценка модели
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Сохранение модели и векторизатора
model_path = os.path.join(current_dir, 'logistic_regression_model.pkl')
vectorizer_path = os.path.join(current_dir, 'tfidf_vectorizer.pkl')

joblib.dump(log_reg, model_path)
joblib.dump(tfidf_vectorizer, vectorizer_path)

print(f'Модель сохранена по пути: {model_path}')
print(f'Векторизатор TFIDF сохранен по пути: {vectorizer_path}')