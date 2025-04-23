import logging
import asyncio

from utils.get_responses import *
from integrations.get_responses.fetchers import get_all_data
from integrations.google_sheets.google_sheets import create_sheets


logging.basicConfig(level=logging.INFO)


# Главный цикл репортера, запускается раз в сутки
async def reporter_loop():

    test_dates = [
        datetime(2025, 4, 20),  # сегодня воскресенье
        datetime(2025, 4, 30),  # последний день месяца
        datetime(2025, 5, 1),   # первый день нового месяца
        datetime(2025, 4, 23),  # обычный день
    ]

    # Тестируем для разных дат
    for test_date in test_dates:
        time_variables = get_active_time_variables(test_date)
        print(f"Тестируем {test_date.strftime('%Y-%m-%d')}: {time_variables}")


        new_data = await get_all_data()
        for time_variable in time_variables:
            await update_stats_sheet(time_variable, new_data)
        print('Данные заполнены!\n')


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
