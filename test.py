import asyncio
import pandas as pd
from settings import settings

from integrations.get_responses.dle import DLEFetcher
from integrations.get_responses.salexy import SalexyFetcher
from integrations.get_responses.wordpress import WordpressFetcher


async def main():

    # Получаем все данные из Wordpress
    domains_wp = ['mostbet-ar.net', '1xbet-ua.com', 'mostbet-bd.biz', 'fallos.ar',
               'mostbetua.org', 'krsk2019.ru', '1wineg.biz', 'mostbet-no.org',
               'onedivision.ru', '1-win.az', '1win-bett.com.br', '1xbet-bangladesh.org',
               '1xbetapk.biz', 'mostbet-es.net', 'mostbet-kz.org', '1xbetfr.org', '1wineg.org',
               'openbugs.net', '1xbet-ar.biz', 'mostbet.spas-extreme.ru', 'mostbetcasino.pl',
               'mostbet-fr.org', 'mostbetcasino.in', 'mostbet-cassino.com.br', 'mostbet-hu.org']
    fetcher_wp = WordpressFetcher(domains_wp, settings.bot.WP_USERNAME, settings.bot.WP_PASSWORD)
    df_wp = await fetcher_wp.fetch_pwa_stats()

    # Получаем все данные из DLE
    domains_dle = ["mostbet-casinokz.kz", "mostbet-bangladesh.org", "1-win-az.org", "wawada.kz",
                   "vavada.es", "1-win-eg.com", "mostbet-maroc.org", "wawada.pl", "pin-co.az"]
    fetcher_dle = DLEFetcher(domains_dle, settings.bot.WP_USERNAME, settings.bot.WP_PASSWORD)
    df_dle = await fetcher_dle.fetch_pwa_stats()

    # Получаем все данные из Salexy
    domains_slx = ["salexy.kz"]
    fetcher_slx = SalexyFetcher(domains_slx)
    df_slx = await fetcher_slx.fetch_pwa_stats()

    result = pd.concat([df_wp, df_dle, df_slx], ignore_index=True)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())