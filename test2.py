import pandas as pd
from integrations.google_sheets.google_sheets import authorize_spreadsheet

# Пример DataFrame
df = pd.DataFrame({
    "Имя": ["Alice", "Bob"],
    "Привычка": ["Медитация", "Фокус"],
    "Дата": ["2025-04-22", "2025-04-22"],
    "Активен": ["Да", "Нет"]
})

# Конвертация: включая заголовки
values = [df.columns.tolist()] + df.values.tolist()

# Вставка
worksheet = authorize_spreadsheet('Лист1')
worksheet.update(range_name="A30", values=values)
