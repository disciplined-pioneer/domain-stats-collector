import gspread
from typing import List
from settings import settings
from google.oauth2.service_account import Credentials
from gspread_formatting import format_cell_range, CellFormat, Color, TextFormat


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


# Создание  нужных листов, согласно списку + настройка стилей
def create_sheets(list_sheets: List[str] = ["Daily_Stats", "Weekly_Stats", "Monthly_Stats"]) -> None:
    spreadsheet = authorize_spreadsheet()

    # Настройка стилей
    header_format = CellFormat(
        backgroundColor=Color(209 / 255, 109 / 255, 107 / 255),
        textFormat=TextFormat(
            foregroundColor=Color(1, 1, 1),  # Белый текст
            bold=True
        ),
        horizontalAlignment="CENTER",
        verticalAlignment="MIDDLE"
    )

    # Проходимся по всем листам
    for sheet in list_sheets:
        try:
            spreadsheet.add_worksheet(title=sheet, rows="100", cols="20")
            worksheet = spreadsheet.worksheet(sheet)
            worksheet.update("A1", [["Timestamp", "Website", "Count", "Delta", "Status"]])
            format_cell_range(worksheet, 'A1:E1', header_format)
            print(f"Лист '{sheet}' успешно создан и отформатирован.")

        except gspread.exceptions.APIError as e:
            print(f"Лист '{sheet}' уже существует или произошла ошибка: {e}")

        except Exception as e:
            print(f"Произолша ошибка: {e}")

    print("Листы успешно созданы.")
