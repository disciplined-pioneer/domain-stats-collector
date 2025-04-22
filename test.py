from integrations.google_sheets.google_sheets import authorize_spreadsheet

worksheet = authorize_spreadsheet("Лист1")
value = worksheet.acell("A2").value
print(value)