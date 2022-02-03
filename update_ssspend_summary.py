
import argparse
import json

from ssspend.spenddataframe import get_google_spreadsheet_from_oauth2, \
    get_google_spreadsheet_from_apikey, get_google_spreadsheet_from_service_account
from ssspend.summarydataframe import generate_summary_dict, generate_summary_df, \
    update_summary_googlespreadsheet

argparser = argparse.ArgumentParser(description='Update SSSpend summary')
argparser.add_argument('url', help='URL of spreadsheet')
argparser.add_argument('--client_json_file', default='client_json.json', help='client_json')
argparser.add_argument('--storage_json', default='storage.json', help='storage_json')
argparser.add_argument('--apikey', default=None, type=str, help='API key')
argparser.add_argument('--serviceaccount', default=None, type=str, help='path of the service account info (*.json)')


if __name__ == '__main__':
    args = argparser.parse_args()

    if args.serviceaccount is not None:
        service_account_info = json.load(open(args.serviceaccount))
        spreadsheet = get_google_spreadsheet_from_service_account(service_account_info, args.url)
    elif args.apikey is None:
        spreadsheet = get_google_spreadsheet_from_oauth2(args.client_json_file, args.storage_json, args.url)
    else:
        spreadsheet = get_google_spreadsheet_from_apikey(args.apikey, args.url)
    monthly_summary_dict = generate_summary_dict(spreadsheet)
    summary_df = generate_summary_df(monthly_summary_dict)
    update_summary_googlespreadsheet(args.url, summary_df, service_account_file=args.serviceaccount)


