import logging
import asyncio

from utils.get_responses import *
from integrations.get_responses.fetchers import get_all_data
from integrations.google_sheets.google_sheets import create_sheets


logging.basicConfig(level=logging.INFO)


# Главный цикл репортера, запускается раз в сутки
async def reporter_loop():

    # Скачиваем данные и добавляем в таблицу
    time_variables = get_active_time_variables()
    new_data = await get_all_data()
    for time_variable in time_variables:
        await update_stats_sheet(time_variable, new_data)
    print('Данные заполнены!')


async def main():
    await reporter_loop()


if __name__ == "__main__":
    try:
        print("\nСкрипт запущен ✅\n")
        create_sheets()  # Создаём листы
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n🛑 Скрипт остановлен 🛑\n")

    except Exception as e:
        print(f"\n❌ Возникла ошибка : {e}\n")
