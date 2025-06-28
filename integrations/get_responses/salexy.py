import asyncio
import aiohttp
import pandas as pd
from datetime import datetime
import logging


class SalexyFetcher:

    """Класс для получения данных с сайтов по их доменам - SALEXY"""

    def __init__(self, domains):
        self.domains = domains
        self.results = []

    # Асинхронная функция для выполнения запросов и сбора данных в DataFrame
    async def fetch_pwa_stats(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for domain in self.domains:
                api_url = f"https://{domain}/custom-api/v1/pwa-install-stats"
                tasks.append(self.fetch_for_domain(session, domain, api_url))
            await asyncio.gather(*tasks)

        # Создание DataFrame из собранных результатов
        df = pd.DataFrame(self.results)
        return df

    # Функция для получения данных с каждого домена
    async def fetch_for_domain(self, session, domain, url):
        try:
            # Отправка GET-запроса
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    result = {
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'Website': domain,
                        'День': data.get('daily', 'error'),
                        'Неделя': data.get('weekly', 'error'),
                        'Месяц': data.get('monthly', 'error'),
                        'Delta': 0,
                        'Status': '✅ OK'
                    }
                else:
                    result = {
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'Website': domain,
                        'День': 0,
                        'Неделя': 0,
                        'Месяц': 0,
                        'Delta': 0,
                        'Status': '❌ ERROR'
                    }
                    logging.error(f"❌ Ошибка для {domain} | {response.status}")
                self.results.append(result)

        except Exception as e:
            result = {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Website': domain,
                'День': 0,
                'Неделя': 0,
                'Месяц': 0,
                'Delta': 0,
                'Status': '❌ ERROR'
            }
            self.results.append(result)
            logging.error(f"❌ Ошибка для {domain} | {e}")
