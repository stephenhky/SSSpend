
from gsheets import Sheets

def get_google_spreadsheet(my_client_secret, my_client_storage, url):
    sheets = Sheets.from_files(my_client_secret, my_client_storage)
    spreadsheet = sheets.get(url)
    return spreadsheet


def get_month_dataframe(spreadsheet, month):
    cols = ['Date', 'Place', 'Category', 'City', 'Debit', 'Comment', 'Individual',
             'Payment Method']
    df = spreadsheet.find(month).to_frame(usecols=cols)
    return df

