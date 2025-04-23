# Statistics 301

Автоматизированный скрипт для сбора статистики по доменам с различных платформ (WordPress, DLE, Salexy) и записи этих данных в Google Sheets. Система работает по расписанию, определяя конец дня, недели и месяца, и заполняет соответствующие листы в таблице.

## 📌 Назначение

- Делает GET-запросы к заранее заданным доменам.
- Извлекает ключевые данные (например, редиректы или статус страниц).
- Записывает результат в Google Sheets: **Daily_Stats**, **Weekly_Stats**, **Monthly_Stats**.
- Работает в автоматическом режиме, запускается ежедневно в 23:55.

---

## 📁 Структура проекта

```bash
.
├─── config
│   ├─── domains_config.json       # JSON-файл с доменами по платформам (WordPress, DLE, Salexy).
│   └─── service_account.json      # Ключ сервисного аккаунта Google для работы с Google Sheets.
├─── integrations
│   ├─── get_responses             # Логика получения данных с сайтов.
│   │   ├─── __init__.py
│   │   ├─── dle.py                # Обработчик доменов на DLE.
│   │   ├─── fetchers.py           # Универсальные функции запроса данных.
│   │   ├─── salexy.py             # Обработчик Salexy-доменов.
│   │   └─── wordpress.py          # Обработчик WordPress-доменов.
│   ├─── google_sheets
│   │   ├─── __init__.py
│   │   └─── google_sheets.py      # Запись статистики в Google Sheets.
│   └─── __init__.py
├─── utils
│   ├─── __init__.py
│   ├─── get_responses.py          # Общие утилиты для сбора ответов.
│   └─── google_sheets.py          # Вспомогательные функции для работы с таблицами.
├─── .env                          # Файл окружения с конфигурацией доступа.
├─── .gitignore                    # Исключает лишние файлы из репозитория.
├─── Dockerfile                    # Docker-окружение для развертывания.
├─── main.py                       # Точка входа. Оркестрация всего процесса.
├─── requirements.txt              # Список зависимостей проекта.
└─── settings.py                   # Загрузка переменных и глобальных параметров.
```

---

## ⚙️ Конфигурация

### `.env`

Шаблон конфигурации:

```env
# WordPress
WP_USERNAME=
WP_PASSWORD=

# Google Sheets
GSHEETS_CREDENTIALS_JSON=config/service_account.json
PATH_ALL_DOMAINS_JSON=config/domains_config.json
SHEETS_NAME= # Название таблицы excel
```

### `domains_config.json`

Пример шаблона (реальные данные не включаются в README):

```json
{
  "Wordpress": ["example1.com", "example2.com"],
  "DLE": ["example3.com"],
  "Salexy": ["example4.com"]
}
```

---

## 🕒 Расписание

Скрипт запускается ежедневно в **23:55**. Определяет:

- Последний день недели → обновляет **Weekly_Stats**
- Последний день месяца → обновляет **Monthly_Stats**
- В любой день → обновляет **Daily_Stats**

---

## 🚀 Запуск

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Настройте `.env` и `domains_config.json` и service_account.json

3. Запустите скрипт вручную или настройте cron/airflow/systemd:

```bash
python main.py
```

---

## 📈 Google Sheets

Скрипт автоматически создает или обновляет листы:

- `Daily_Stats`
- `Weekly_Stats`
- `Monthly_Stats`

Каждый лист содержит актуальную статистику по доменам в соответствии с датой запуска, а затем добавляет стили