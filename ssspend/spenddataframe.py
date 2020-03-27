
import pandas as pd
from gsheets import Sheets

def get_google_spreadsheet(my_client_secret, my_client_storage, url):
    sheets = Sheets.from_files(my_client_secret, my_client_storage)
    spreadsheet = sheets.get(url)
    return spreadsheet


def get_month_dataframe(spreadsheet, month):
    df = spreadsheet.find(month).to_frame(index_col='Unnamed: 0')
    df = df[['Date', 'Place', 'Category', 'City', 'Debit', 'Comment', 'Individual',
             'Payment Method']]
    return df

