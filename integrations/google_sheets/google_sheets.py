import gspread
from typing import List
import unicodedata
from settings import settings
from gspread_formatting import *
from google.oauth2.service_account import Credentials

import logging
import traceback

from gspread_formatting import (
    get_conditional_format_rules,
    ConditionalFormatRule,
    BooleanRule,
    CellFormat,
    Color,
    BooleanCondition,
    GridRange
)

# Настроим логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Нормализация для проверки слов
def normalize(s):
    return unicodedata.normalize('NFKC', s.strip())


# Функция для создания таблицы
def create_spreadsheet(spreadsheet_name: str) -> gspread.Spreadsheet:

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    credentials = Credentials.from_service_account_file(
        settings.bot.GSHEETS_CREDENTIALS_JSON,
        scopes=scopes
    )
    
    client = gspread.authorize(credentials)

    # Проверка, существует ли таблица с таким именем
    try:
        spreadsheet = client.open(spreadsheet_name)
        logging.info(f"Таблица '{spreadsheet_name}' уже существует.")

    except gspread.exceptions.SpreadsheetNotFound:
        logging.info(f"Таблица '{spreadsheet_name}' не найдена. Создаём новую.")
        spreadsheet = client.create(spreadsheet_name)

        # Делает таблицу доступной владельцу по email
        spreadsheet.share('maksimsarsov777@gmail.com', perm_type='user', role='writer')
        #spreadsheet.share('analytics@analyzer-sheets-453416.iam.gserviceaccount.com', perm_type='user', role='writer')

    return spreadsheet


# Настраиваем доступ к Google Sheets через google-auth
def authorize_spreadsheet(SHEETS_NAME=settings.bot.SHEETS_NAME):

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_file(
        settings.bot.GSHEETS_CREDENTIALS_JSON,
        scopes=scopes
    )

    client = gspread.authorize(credentials)
    return client.open(SHEETS_NAME)


# Создание нужных листов, согласно списку + настройка стилей
def create_sheets(list_sheets: List[str] = ["День", "Неделя", "Месяц"]) -> None:

    spreadsheet = authorize_spreadsheet()

    # Настройка стиля заголовков
    header_format = CellFormat(
        backgroundColor=Color(209 / 255, 109 / 255, 107 / 255),  # Розово-красный
        textFormat=TextFormat(
            foregroundColor=Color(1, 1, 1),  # Белый текст
            bold=True
        ),
        horizontalAlignment="CENTER",
        verticalAlignment="MIDDLE"
    )

    for sheet_title in list_sheets:
        worksheet = None
        try:
            worksheet = spreadsheet.worksheet(sheet_title)
            logging.info(f"Лист '{sheet_title}' уже существует.")
        except gspread.exceptions.WorksheetNotFound:

            # Создание
            worksheet = spreadsheet.add_worksheet(title=sheet_title, rows="1000", cols="20")
            logging.info(f"Лист '{sheet_title}' создан.")

            # Форматирование
            apply_conditional_formatting(worksheet)
            worksheet.update("A1:E1", [["Timestamp", "Website", "Count", "Delta", "Status"]])
            format_cell_range(worksheet, 'A1:E1', header_format)
            logging.info(f"Лист '{sheet_title}' отформатирован.")

        except Exception as e:
            traceback.print_exc()
            logging.error(f"Ошибка при настройке листа '{sheet_title}': {str(e)}")

    logging.info("Создание и настройка всех листов завершена.")


# Закрашиваем ячейки нужными цветами
def apply_conditional_formatting(worksheet: gspread.Worksheet):
    sheet_id = worksheet._properties['sheetId']
    rules = get_conditional_format_rules(worksheet)
    rules.clear()

    # Центрирование текста, перенос и выравнивание по середине (A–E)
    requests = [{
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "startColumnIndex": 0,
                "endColumnIndex": 5
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE",
                    "wrapStrategy": "WRAP"
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"
        }
    }]

    # Устанавливаем высоту всех строк = 40
    for row in range(0, worksheet.row_count):
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": row,
                    "endIndex": row + 1
                },
                "properties": {
                    "pixelSize": 40
                },
                "fields": "pixelSize"
            }
        })

    # Устанавливаем ширину колонки B (индекс 1) на 175
    requests.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 1,
                "endIndex": 2
            },
            "properties": {
                "pixelSize": 175
            },
            "fields": "pixelSize"
        }
    })

    # Автоматическая ширина остальных колонок A, C, D, E
    requests.append({
        "autoResizeDimensions": {
            "dimensions": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": 1
            }
        }
    })

    requests.append({
        "autoResizeDimensions": {
            "dimensions": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 2,
                "endIndex": 5
            }
        }
    })

    # Условное форматирование
    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=3, endColumnIndex=4)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='NUMBER_EQ', values=['0']),
            format=CellFormat(backgroundColor=Color(0.86, 0.86, 0.86))
        )
    ))

    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=3, endColumnIndex=4)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='NUMBER_GREATER', values=['0']),
            format=CellFormat(backgroundColor=Color(0.6, 0.9, 0.6))
        )
    ))

    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=3, endColumnIndex=4)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='NUMBER_LESS', values=['0']),
            format=CellFormat(backgroundColor=Color(0.95, 0.6, 0.6))
        )
    ))

    rules.append(ConditionalFormatRule(
        ranges=[GridRange(sheetId=sheet_id, startRowIndex=1, startColumnIndex=0, endColumnIndex=5)],
        booleanRule=BooleanRule(
            condition=BooleanCondition(type='CUSTOM_FORMULA', values=['=$E2="❌ ERROR"']),
            format=CellFormat(backgroundColor=Color(0.86, 0.86, 0.86))
        )
    ))

    # Применяем правила и стили
    rules.save()

    # Сначала применим стили (высота, wrap, выравнивание)
    authorize_spreadsheet().batch_update({'requests': requests[:-1]})

    # Затем отдельно автоширину для колонок A, C, D, E и устанавливаем ширину для B
    authorize_spreadsheet().batch_update({'requests': requests[-2:]})

