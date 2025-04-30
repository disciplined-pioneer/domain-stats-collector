import logging
import asyncio
from datetime import datetime, timedelta

from settings import settings
from utils.get_responses import *
from integrations.get_responses.fetchers import get_all_data
from integrations.google_sheets.google_sheets import create_sheets, create_spreadsheet


# Настроим логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Ожидание до 23:55
async def wait_until_midnight():
    now = datetime.now()
    MINUTE, HOUR = map(int, settings.bot.CHECK_INTERVAL_DAILY_CRON.split()[:2])
    logging.info(f'Запуск скрипта в {HOUR}:{MINUTE}')
    future = now.replace(hour=HOUR, minute=MINUTE, second=0, microsecond=0)
    if future <= now:
        future += timedelta(days=1)
    await asyncio.sleep((future - now).total_seconds())


# Главный цикл репортера, запускается раз в сутки
async def reporter_loop():
    while True:
        try:
            await wait_until_midnight()  # Ожидаем нужного времени

            # Скачиваем данные и добавляем в таблицу
            time_variables = get_active_time_variables()
            new_data = await get_all_data()
            for time_variable in time_variables:
                await update_stats_sheet(time_variable, new_data)
            logging.info('Данные заполнены!')

        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")


async def main():
    await reporter_loop()


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
