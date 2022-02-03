
import argparse
import json
import os
import logging

import boto3

from ssspend.spenddataframe import get_google_spreadsheet_from_oauth2, \
    get_google_spreadsheet_from_apikey, get_google_spreadsheet_from_service_account
from ssspend.summarydataframe import generate_summary_dict, generate_summary_df, \
    update_summary_googlespreadsheet

argparser = argparse.ArgumentParser(description='Update SSSpend summary')
argparser.add_argument('url', help='URL of spreadsheet')
argparser.add_argument('--serviceaccount', default=None, type=str, help='path of the service account info (*.json)')


def lambda_handler(event, context):
    # getting query
    logging.info(event)
    logging.info(context)
    query = json.loads(event['body'])
    url = query['url']
    logging.info('spreadsheet URL: {}'.format(url))

    # getting environment variables
    s3_bucket_name = os.environ.get('s3_bucket')
    service_account_file = os.environ.get('service_account_file')

    # get service account info
    s3_client = boto3.client('s3')
    s3_client.download_file(s3_bucket_name, service_account_file, 'service_account.json')
    service_account_info = json.load(open('service_account.json', 'r'))

    # handling Google spreadsheet
    spreadsheet = get_google_spreadsheet_from_service_account(service_account_info, url)
    monthly_summary_dict = generate_summary_dict(spreadsheet)
    summary_df = generate_summary_df(monthly_summary_dict)
    update_summary_googlespreadsheet(url, summary_df, service_account_file='service_account.json')

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'body': json.dumps(event)
    }

