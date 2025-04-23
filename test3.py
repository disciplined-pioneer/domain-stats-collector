import asyncio
import pandas as pd
from integrations.get_responses.fetchers import get_all_data
from integrations.google_sheets.google_sheets import get_sheet_data_as_df, authorize_spreadsheet

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

    # Приводим 'Count' и 'Delta' к строковому типу, чтобы избежать проблем при замене значений
    df['Count'] = df['Count'].astype(str)
    df['Delta'] = df['Delta'].astype(str)

    # Сортируем по Timestamp
    df = df.sort_values(by=['Timestamp', 'Website'])

    # Заменяем значения на '-' в строках с ошибкой
    df.loc[df['Status'] == '❌ ERROR', ['Count', 'Delta']] = '-'

    # Заменяем NaN на '0' в Delta
    df['Delta'] = df['Delta'].replace('nan', '0')

    # Заполняем NaN значениями '-'
    df.fillna('-', inplace=False)

    # Преобразуем 'Timestamp' обратно в строку, если нужно
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%dT%H:%M:%S').dt.strftime('%Y-%m-%d %H:%M')


    return df




async def main(time_variable: str):

    # Получаем все данные из доменов + excel
    name_sheet = f"{time_variable.capitalize()}_Stats"
    old_df = await get_sheet_data_as_df(name_sheet)
    new_df = await get_all_data()
    df = new_df[["Timestamp", "Website", time_variable, 'Delta', "Status"]].rename(columns={time_variable: "Count"})

    # Преобразование и добавление данных
    result = await data_merging(old_df, df)
    values = [result.columns.tolist()] + result.values.tolist()
    worksheet = authorize_spreadsheet().worksheet(name_sheet)
    worksheet.update(range_name="A1", values=values)
    

if __name__ == "__main__":
    time_variable = 'weekly'
    asyncio.run(main(time_variable))