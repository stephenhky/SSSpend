
from gsheets import Sheets
from google.oauth2 import service_account


def get_google_spreadsheet_from_oauth2(my_client_secret, my_client_storage, url):
    sheets = Sheets.from_files(my_client_secret, my_client_storage)
    spreadsheet = sheets.get(url)
    return spreadsheet


def get_google_spreadsheet_from_apikey(apikey, url):
    sheets = Sheets.from_developer_key(apikey)
    spreadsheet = sheets.get(url)
    return spreadsheet


def get_google_spreadsheet_from_service_account(service_account_info, url):
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    sheets = Sheets(credentials)
    spreadsheet = sheets.get(url)
    return spreadsheet


def get_month_dataframe(spreadsheet, month):
    cols = ['Date', 'Place', 'Category', 'City', 'Debit', 'Comment', 'Individual',
             'Payment Method']
    df = spreadsheet.find(month).to_frame(usecols=cols)
    return df

