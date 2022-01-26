
import argparse

from ssspend.spenddataframe import get_google_spreadsheet_from_oauth2, get_google_spreadsheet_from_apikey
from ssspend.summarydataframe import generate_summary_dict, generate_summary_df, \
    update_summary_googlespreadsheet

argparser = argparse.ArgumentParser(description='Update SSSpend summary')
argparser.add_argument('url', help='URL of spreadsheet')
argparser.add_argument('--client_json_file', default='client_json.json', help='client_json')
argparser.add_argument('--storage_json', default='storage.json', help='storage_json')
argparser.add_argument('--apikey', default=None, type=str, help='API key')


if __name__ == '__main__':
    args = argparser.parse_args()

    if args.apikey is None:
        spreadsheet = get_google_spreadsheet_from_oauth2(args.client_json_file, args.storage_json, args.url)
    else:
        spreadsheet = get_google_spreadsheet_from_apikey(args.apikey, args.url)
    monthly_summary_dict = generate_summary_dict(spreadsheet)
    summary_df = generate_summary_df(monthly_summary_dict)
    update_summary_googlespreadsheet(args.url, summary_df)


