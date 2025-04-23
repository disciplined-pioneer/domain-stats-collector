import pandas as pd
from integrations.google_sheets.google_sheets import authorize_spreadsheet


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