import gspread
from typing import List
import unicodedata
from settings import settings
from gspread_formatting import *
from google.oauth2.service_account import Credentials

from gspread_formatting import (
    get_conditional_format_rules,
    ConditionalFormatRule,
    BooleanRule,
    CellFormat,
    Color,
    BooleanCondition,
    GridRange
)


# Нормализация для проверки слов
def normalize(s):
    return unicodedata.normalize('NFKC', s.strip())


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
            spreadsheet.add_worksheet(title=sheet, rows="1000", cols="20")
            worksheet = spreadsheet.worksheet(sheet)
            worksheet.update("A1", [["Timestamp", "Website", "Count", "Delta", "Status"]])
            format_cell_range(worksheet, 'A1:E1', header_format)
            print(f"Лист '{sheet}' успешно создан и отформатирован.")

        except gspread.exceptions.APIError as e:
            print(f"Лист '{sheet}' уже существует или произошла ошибка: {e}")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        apply_conditional_formatting(sheet) # Настраиваем окрашивания

    print("Листы успешно созданы.")


# Закрашиваем ячейки нужными цветами
def apply_conditional_formatting(sheet_name):
    
    worksheet = authorize_spreadsheet().worksheet(sheet_name)
    sheet_id = worksheet._properties['sheetId']
    rules = get_conditional_format_rules(worksheet)

    # Очистим старые правила, если нужно
    rules.clear()

    # D column: Delta == 0 — серый
    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=3, endColumnIndex=4)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='NUMBER_EQ', values=['0']),  # Для чисел, равных '0'
            format=CellFormat(backgroundColor=Color(1, 1, 1))  # Белый цвет
        )
    ))


    # D column: Delta > 0 — зелёный
    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=3, endColumnIndex=4)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='NUMBER_GREATER', values=['0']),  # Для чисел, больше '0' (как строка)
            format=CellFormat(backgroundColor=Color(0.6, 0.9, 0.6))  # Зеленый
        )
    ))

    # D column: Delta < 0 — красный
    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=3, endColumnIndex=4)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='NUMBER_LESS', values=['0']),  # Для чисел, меньше '0' (как строка)
            format=CellFormat(backgroundColor=Color(0.95, 0.6, 0.6))  # Красный
        )
    ))

    # E column: Status == ❌ ERROR — серый
    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=4, endColumnIndex=5)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='TEXT_EQ', values=['❌ ERROR']),
            format=CellFormat(backgroundColor=Color(0.85, 0.85, 0.85))
        )
    ))

    rules.save()
