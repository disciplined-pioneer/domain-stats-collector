import time
import asyncio
import aiohttp
import pandas as pd
from aiohttp import BasicAuth


class DLEFetcher:

    """Класс для получения данных с сайтов по их доменам - DLE"""

    def __init__(self, domains, username, password):
        self.domains = domains
        self.username = username
        self.password = password
        self.results = []

    # Асинхронная функция для выполнения запросов и сбора данных в DataFrame
    async def fetch_pwa_stats(self):
        auth = BasicAuth(self.username, self.password)
        async with aiohttp.ClientSession(auth=auth) as session:
            tasks = []
            
            for domain in self.domains:
                api_url = f"https://{domain}/api.php?action=get_pwa_install_stats"
                tasks.append(self.fetch_for_domain(session, domain, api_url))
            await asyncio.gather(*tasks)

        # Создание DataFrame из собранных результатов
        df = pd.DataFrame(self.results)
        return df

    # Функция для получения данных с каждого домена
    async def fetch_for_domain(self, session, domain, url):
        data = {
            'username': self.username,
            'password': self.password
        }
        
        try:
            # Отправка POST-запроса
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    data = await response.json()
                    result = {
                        'Timestamp': time.time(),
                        'Website': domain,
                        'daily': data.get('daily', 'error'),
                        'weekly': data.get('weekly', 'error'),
                        'monthly': data.get('monthly', 'error'),
                        'Status': 'ОК!'
                    }
                else:
                    result = {
                        'Timestamp': time.time(),
                        'Website': domain,
                        'daily': '-',
                        'weekly': '-',
                        'monthly': '-',
                        'Status': '❌ ERROR'
                    }
                    print(f"❌ Ошибка для {domain}: {response.status}")
                self.results.append(result)

        except Exception as e:
            result = {
                'Timestamp': time.time(),
                'Website': domain,
                'daily': '-',
                'weekly': '-',
                'monthly': '-',
                'Status': '❌ ERROR'
            }
            self.results.append(result)
            print(f"❌ Ошибка для {domain}: {e}")
