import requests
from requests.auth import HTTPBasicAuth


# URL для получения текущего PWA URL
#api_url = "https://krsk2019.ru/wp-json/custom-api/v1/pwa-install-stats/"
api_url = "https://krsk2019.ru/wp-json/custom-api/v1/pwa-url/"

# Отправка GET-запроса с аутентификацией
response = requests.get(api_url, auth=HTTPBasicAuth('admin', 'xit4t1L_Er'))

# Проверка статуса ответа
if response.status_code == 200:
    print("Гуд! Ответ сервера:", response.json())  # Выводим JSON-ответ
else:
    print("Ошибка:", response.text)  # Выводим текст ошибки
