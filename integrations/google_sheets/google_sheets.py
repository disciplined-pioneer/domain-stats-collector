import gspread
import pandas as pd
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


# Нормализация строки
def normalize_row(row, length):
    row = [cell if cell is not None else '-' for cell in row]  # заменяем None на '-'
    return row + ['-'] * (length - len(row))


# Получение значений из диапазона колонок
async def get_sheet_data_as_df(sheet_name: str) -> pd.DataFrame:

    spreadsheet = authorize_spreadsheet()
    sheet = spreadsheet.worksheet(sheet_name)

    values = sheet.get("A:E")

    # Обработка случая, если вообще нет данных
    if not values or all(not any(str(cell).strip() for cell in row) for row in values):
        return pd.DataFrame()

    headers = [h if h is not None else '' for h in values[0]]
    data = [normalize_row(row, len(headers)) for row in values[1:]]
    
    # Преобразование данных в DataFrame и замена NaN значений
    df = pd.DataFrame(data, columns=headers)
    df = df.fillna('-')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce', dayfirst=False)
    df['Count'] = df['Count'].replace('-', 0)

    return df