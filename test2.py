import pandas as pd
from integrations.google_sheets.google_sheets import authorize_spreadsheet

import pandas as pd

data = [
    ["2025-04-23 13:56", "mostbetua.org", 0, 5, 15, "ОК!"],
    ["2025-04-23 13:56", "1xbet-bangladesh.org", 0, 3, 12, "ОК!"],
    ["2025-04-23 13:56", "1wineg.org", "-", "-", "-", "❌ ERROR"],
    ["2025-04-23 13:56", "1xbetapk.biz", 0, 0, 7, "ОК!"],
    ["2025-04-23 13:56", "krsk2019.ru", 0, 0, 2, "ОК!"],
    ["2025-04-23 13:56", "onedivision.ru", 0, 0, 0, "ОК!"],
    ["2025-04-23 13:56", "mostbet-kz.org", 0, 0, 1, "ОК!"],
    ["2025-04-23 13:56", "1xbetfr.org", 0, 1, 14, "ОК!"],
    ["2025-04-23 13:56", "1xbet-ar.biz", 1, 44, 163, "ОК!"],
    ["2025-04-23 13:56", "fallos.ar", 0, 0, 0, "ОК!"],
    ["2025-04-23 13:56", "1xbet-ua.com", 0, 0, 5, "ОК!"],
    ["2025-04-23 13:56", "1wineg.biz", 0, 0, 0, "ОК!"],
    ["2025-04-23 13:56", "1-win.az", 0, 1, 1, "ОК!"],
    ["2025-04-23 13:56", "openbugs.net", 0, 4, 15, "ОК!"],
    ["2025-04-23 13:56", "mostbet-hu.org", 0, 0, 0, "ОК!"],
    ["2025-04-23 13:56", "mostbet.spas-extreme.ru", "-", "-", "-", "❌ ERROR"],
    ["2025-04-23 13:56", "mostbetcasino.pl", 0, 0, 3, "ОК!"],
    ["2025-04-23 13:56", "mostbet-cassino.com.br", 0, 1, 1, "ОК!"],
    ["2025-04-23 13:56", "1win-bett.com.br", 0, 0, 3, "ОК!"],
    ["2025-04-23 13:56", "mostbet-ar.net", 0, 1, 10, "ОК!"],
    ["2025-04-23 13:56", "mostbet-no.org", 0, 0, 0, "ОК!"],
    ["2025-04-23 13:56", "mostbetcasino.in", 0, 0, 13, "ОК!"],
    ["2025-04-23 13:56", "mostbet-es.net", 0, 0, 1, "ОК!"],
    ["2025-04-23 13:56", "mostbet-fr.org", 0, 1, 1, "ОК!"],
    ["2025-04-23 13:56", "mostbet-bd.biz", 0, 25, 70, "ОК!"],
    ["2025-04-23 13:56", "1-win-az.org", "-", "-", "-", "❌ ERROR"],
    ["2025-04-23 13:56", "1-win-eg.com", "-", "-", "-", "❌ ERROR"],
    ["2025-04-23 13:56", "mostbet-bangladesh.org", 0, 1, 4, "ОК!"],
    ["2025-04-23 13:56", "mostbet-maroc.org", 0, 2, 11, "ОК!"],
    ["2025-04-23 13:56", "pin-co.az", 0, 0, 0, "ОК!"],
    ["2025-04-23 13:56", "mostbet-casinokz.kz", 0, 0, 1, "ОК!"],
    ["2025-04-23 13:56", "wawada.pl", 0, 1, 11, "ОК!"],
    ["2025-04-23 13:56", "wawada.kz", 0, 0, 1, "ОК!"],
    ["2025-04-23 13:56", "vavada.es", 0, 0, 1, "ОК!"],
    ["2025-04-23 13:56", "salexy.kz", "-", "-", "-", "❌ ERROR"],
]

columns = ['Timestamp', 'Website', 'daily', 'weekly', 'monthly', 'Status']

df = pd.DataFrame(data, columns=columns)


# Конвертация: включая заголовки
values = [df.columns.tolist()] + df.values.tolist()

# Вставка
worksheet = authorize_spreadsheet().worksheet('Monthly_Stats')
worksheet.update(range_name="A1", values=values)
