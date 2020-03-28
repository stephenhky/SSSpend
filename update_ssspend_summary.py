
import argparse

from ssspend.spenddataframe import get_google_spreadsheet
from ssspend.summarydataframe import generate_summary_dict, generate_summary_df, \
    update_summary_googlespreadsheet

argparser = argparse.ArgumentParser(description='Update SSSpend summary')
argparser.add_argument('url', help='URL of spreadsheet')
argparser.add_argument('--client_json_file', default='client_json.json', help='client_json')
argparser.add_argument('--storage_json', default='storage.json', help='storage_json')


if __name__ == '__main__':
    args = argparser.parse_args()

    spreadsheet = get_google_spreadsheet(args.client_json_file, args.storage_json, args.url)
    monthly_summary_dict = generate_summary_dict(spreadsheet)
    summary_df = generate_summary_df(monthly_summary_dict)
    update_summary_googlespreadsheet(args.url, summary_df)


