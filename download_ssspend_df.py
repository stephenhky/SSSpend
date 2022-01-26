
import argparse

from ssspend.spenddataframe import get_google_spreadsheet_from_oauth2, get_month_dataframe
from ssspend.knowledge import months


argparser = argparse.ArgumentParser(description='Update SSSpend summary')
argparser.add_argument('url', help='URL of spreadsheet')
argparser.add_argument('datapath', help='path of dataframe')
argparser.add_argument('--client_json_file', default='client_json.json', help='client_json')
argparser.add_argument('--storage_json', default='storage.json', help='storage_json')
argparser.add_argument('--xlsx', default=False, action='store_true', help='Save as an Excel file (default is CSV)')


if __name__ == '__main__':
    args = argparser.parse_args()

    spreadsheet = get_google_spreadsheet_from_oauth2(args.client_json_file, args.storage_json, args.url)
    dataframes = [get_month_dataframe(spreadsheet, month) for month in months]
    combined_dataframe = dataframes[0]
    for dataframe in dataframes[1:]:
        combined_dataframe = combined_dataframe.append(dataframe)

    if args.xlsx:
        combined_dataframe.to_excel(args.datapath)
    else:
        combined_dataframe.to_csv(args.datapath)

