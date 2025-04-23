import asyncio
from integrations.get_responses.fetchers import get_all_data

async def main():
    df = await get_all_data()
    print(df)

if __name__ == "__main__":
    asyncio.run(main())