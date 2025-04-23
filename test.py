import time
import asyncio
from utils.get_responses import *
from integrations.get_responses.fetchers import get_all_data
from integrations.google_sheets.google_sheets import create_sheets


async def main():
    create_sheets()
    time_variable_list = ['daily', 'weekly', 'monthly']
    new_data = await get_all_data()
    for time_variable in time_variable_list:
        await update_stats_sheet(time_variable, new_data)
    

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end-start)