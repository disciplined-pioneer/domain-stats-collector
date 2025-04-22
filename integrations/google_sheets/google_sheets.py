import gspread
from typing import List
from settings import settings
from google.oauth2.service_account import Credentials


# Настраиваем доступ к Google Sheets через google-auth
def authorize_spreadsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_file(
        settings.bot.GSHEETS_CREDENTIALS_JSON,
        scopes=scopes
    )

    client = gspread.authorize(credentials)
    return client.open(settings.bot.SHEETS_NAME)


# Создание  нужных листов, согласно списку
def create_sheets(list_sheets: List[str] = ["Daily_Stats", "Weekly_Stats", "Monthly_Stats"]) -> None:

    spreadsheet = authorize_spreadsheet()

    # Проходим по списку листов и создаем каждый
    for sheet in list_sheets:
        try:
            # Проверяем, существует ли уже лист с таким названием
            spreadsheet.add_worksheet(title=sheet, rows="100", cols="20")
            print(f"Лист '{sheet}' успешно создан.")

        except gspread.exceptions.APIError as e:
            # Если лист с таким названием уже существует
            print(f"Лист '{sheet}' уже существует или произошла ошибка: {e}")

    print("Листы успешно созданы.")