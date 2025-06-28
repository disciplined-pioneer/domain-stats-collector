import pandas as pd
from datetime import datetime, timedelta
from utils.google_sheets import get_sheet_data_as_df
from integrations.google_sheets.google_sheets import authorize_spreadsheet, apply_conditional_formatting


# Объедение старых данных (excel), с новыми из запроса
async def data_merging(old_df, new_df):

    old_df = old_df.copy()
    new_df = new_df.copy()

    # Удаляем строки с отсутствующим Website или Count
    old_df.replace('-', None, inplace=True)
    new_df.replace('-', None, inplace=True)
    
    # Сортируем по названию сайта
    old_df = old_df.sort_values(by=['Website'])
    new_df = new_df.sort_values(by=['Website'])

    # Преобразуем типы
    old_df['Timestamp'] = pd.to_datetime(old_df['Timestamp'])
    new_df['Timestamp'] = pd.to_datetime(new_df['Timestamp'])
    old_df['Count'] = pd.to_numeric(old_df['Count'], errors='coerce')
    new_df['Count'] = pd.to_numeric(new_df['Count'], errors='coerce')

    # Получаем последние Count из old_df по каждому Website
    last_old = old_df.sort_values('Timestamp').groupby('Website').last().reset_index()
    last_old = last_old[['Website', 'Count']].rename(columns={'Count': 'PreviousCount'})

    # Присоединяем к new_df последнюю старую Count по Website
    new_df = new_df.merge(last_old, on='Website', how='left')

    # Вычисляем дельту
    new_df['Delta'] = new_df['Count'] - new_df['PreviousCount']
    new_df['Delta'] = new_df['Delta'].fillna(0).apply(lambda x: 0 if x == 0.0 else x)

    # Убираем вспомогательное поле
    new_df.drop(columns=['PreviousCount'], inplace=True)

    # Форматируем дату, если нужно
    new_df['Timestamp'] = new_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')

    return new_df


# Функция для добавления данных в таблицу excel
async def update_stats_sheet(time_variable: str, new_data: pd.DataFrame):

    # Получаем все данные из доменов
    name_sheet = f"{time_variable.capitalize()}"
    old_df = await get_sheet_data_as_df(name_sheet)
    df = new_data[["Timestamp", "Website", time_variable, 'Delta', "Status"]].rename(columns={time_variable: "Count"})
    
    # Преобразование и добавление данных
    result = await data_merging(old_df, df)
    values = [result.columns.tolist()] + result.values.tolist()
    worksheet = authorize_spreadsheet().worksheet(name_sheet)
    worksheet.update(range_name="A1", values=values)


# Получение списка нужных значений
def get_active_time_variables(today: datetime = None) -> list[str]:
    
    if today is None:
        today = datetime.today()

    result = ['День']  # всегда делаем daily

    # Если сегодня воскресенье — добавляем weekly
    if today.weekday() == 6:
        result.append('Неделя')

    # Если завтра уже другой месяц — добавляем monthly
    tomorrow = today + timedelta(days=1)
    if tomorrow.month != today.month:
        result.append('Месяц')

    return result