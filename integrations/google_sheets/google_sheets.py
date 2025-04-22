import gspread
from settings import settings
from google.oauth2.service_account import Credentials


# Настраиваем доступ к Google Sheets через google-auth
def authorize_spreadsheet(worksheet: str):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_file(
        settings.bot.GSHEETS_CREDENTIALS_JSON,
        scopes=scopes
    )

    client = gspread.authorize(credentials)
    return client.open(settings.bot.SHEETS_NAME).worksheet(worksheet)
