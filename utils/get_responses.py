import pandas as pd
from datetime import datetime, timedelta
from utils.google_sheets import get_sheet_data_as_df
from integrations.google_sheets.google_sheets import authorize_spreadsheet, apply_conditional_formatting


# Объедение старых данных (excel), с новыми из запроса
async def data_merging(old_df, new_df):

    # Конкатенация DataFrame
    df = pd.concat([old_df, new_df], ignore_index=True)
    df.replace('-', None, inplace=True)

    # Преобразуем 'Timestamp' в datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Сортируем по Website и Timestamp и вычисляем Delta
    df = df.sort_values(by=['Website', 'Timestamp'])
    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    df['Delta'] = df.groupby('Website')['Count'].diff()

    # Сортируем по Timestamp
    df = df.sort_values(by=['Timestamp', 'Website'])

    # Заменяем NaN на '0' в Delta
    df['Delta'] = df['Delta'].replace('nan', '0')
    df['Delta'] = df['Delta'].fillna(0)
    df['Delta'] = df['Delta'].apply(lambda x: 0 if x == 0.0 else x)

    # Заполняем NaN значениями '-'
    df.fillna('-', inplace=False)

    # Преобразуем 'Timestamp' обратно в строку, если нужно
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%dT%H:%M:%S').dt.strftime('%Y-%m-%d %H:%M')


    return df


# Функция для добавления данных в таблицу excel
async def update_stats_sheet(time_variable: str, new_data: pd.DataFrame):

    # Получаем все данные из доменов + excel
    name_sheet = f"{time_variable.capitalize()}"
    old_df = await get_sheet_data_as_df(name_sheet)
    df = new_data[["Timestamp", "Website", time_variable, 'Delta', "Status"]].rename(columns={time_variable: "Count"})

    # Преобразование и добавление данных
    result = await data_merging(old_df, df)
    values = [result.columns.tolist()] + result.values.tolist()
    worksheet = authorize_spreadsheet().worksheet(name_sheet)
    worksheet.update(range_name="A1", values=values)


# Получение списка нужных значений
def get_active_time_variables(today: datetime = datetime.today()) -> list[str]:

    result = ['День']  # всегда делаем daily

    # Если сегодня воскресенье — добавляем weekly
    if today.weekday() == 6:
        result.append('Неделя')

    # Если завтра уже другой месяц — добавляем monthly
    tomorrow = today + timedelta(days=1)
    if tomorrow.month != today.month:
        result.append('Месяц')

    return result