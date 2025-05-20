import logging
import asyncio
import time
from datetime import datetime

from utils.get_responses import *
from integrations.get_responses.fetchers import get_all_data
from integrations.google_sheets.google_sheets import create_sheets, create_spreadsheet

from settings import settings


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Главный цикл репортера, запускается раз в сутки
async def reporter_loop():

    test_dates = [
        datetime(2025, 4, 30),  # последний день месяца
        datetime(2025, 4, 27),  # воскресенье
    ]

    # Тестируем для разных дат
    for test_date in test_dates:
        time_variables = get_active_time_variables(test_date)
        logging.info(f"Тестируем {test_date.strftime('%Y-%m-%d')}: {time_variables}")

        new_data = await get_all_data()
        for time_variable in time_variables:
            await update_stats_sheet(time_variable, new_data)
        logging.info('Данные заполнены!')


# Главная функция для запуска цикла репортера
async def main():
    await reporter_loop()


# Запуск скрипта
if __name__ == "__main__":
    try:
        logging.info("Скрипт запущен ✅\n")
        sheet_name = settings.bot.SHEETS_NAME
        spreadsheet = create_spreadsheet(sheet_name)  # Создаём таблицу
        create_sheets()  # Создаём листы
        asyncio.run(main())

    except KeyboardInterrupt:
        logging.info("\n🛑 Скрипт остановлен 🛑\n")

    except Exception as e:
        logging.error(f"\n❌ Возникла ошибка : {e}\n")
