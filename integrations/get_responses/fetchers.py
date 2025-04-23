import json
import pandas as pd
from settings import settings

from integrations.get_responses.dle import DLEFetcher
from integrations.get_responses.salexy import SalexyFetcher
from integrations.get_responses.wordpress import WordpressFetcher


# Получаем данных из json файла
async def load_json_data(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


# Получаем все данные по доменам
async def get_all_data():

    domains = await load_json_data(settings.bot.PATH_ALL_DOMAINS_JSON)

    # Получаем все данные из Wordpress
    fetcher_wp = WordpressFetcher(domains.get("Wordpress", []), settings.bot.WP_USERNAME, settings.bot.WP_PASSWORD)
    df_wp = await fetcher_wp.fetch_pwa_stats()

    # Получаем все данные из DLE
    fetcher_dle = DLEFetcher(domains.get("DLE", []), settings.bot.WP_USERNAME, settings.bot.WP_PASSWORD)
    df_dle = await fetcher_dle.fetch_pwa_stats()

    # Получаем все данные из Salexy
    fetcher_slx = SalexyFetcher(domains.get("Salexy", []))
    df_slx = await fetcher_slx.fetch_pwa_stats()

    result = pd.concat([df_wp, df_dle, df_slx], ignore_index=True)
    return result
