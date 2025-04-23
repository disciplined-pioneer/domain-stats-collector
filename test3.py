import asyncio
from integrations.google_sheets.google_sheets import get_sheet_data_as_df

async def main():
    columns_data = await get_sheet_data_as_df("Monthly_Stats")
    print(columns_data)

if __name__ == "__main__":
    asyncio.run(main())