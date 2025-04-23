import time
import asyncio
from utils.get_responses import *
from datetime import datetime, timedelta
from integrations.get_responses.fetchers import get_all_data
from integrations.google_sheets.google_sheets import create_sheets


# Получение списка нужных значений
def get_active_time_variables() -> list[str]:

    today = datetime.today()
    result = ['daily']  # всегда делаем daily

    # Если сегодня воскресенье — добавляем weekly
    if today.weekday() == 6:
        result.append('weekly')

    # Если завтра уже другой месяц — добавляем monthly
    tomorrow = today + timedelta(days=1)
    if tomorrow.month != today.month:
        result.append('monthly')

    return result


async def main():

    # Создаём листы
    create_sheets()

    # Скачаиваем данные и добавляем в таблицу
    time_variables = get_active_time_variables()
    new_data = await get_all_data()
    for time_variable in time_variables:
        await update_stats_sheet(time_variable, new_data)
    

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end-start)