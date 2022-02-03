
import json
import os
import logging

import boto3

from ssspend.spenddataframe import get_google_spreadsheet_from_service_account
from ssspend.summarydataframe import generate_summary_dict, generate_summary_df, \
    update_summary_googlespreadsheet


service_account_filename = 'service_account.json'


def lambda_handler(event, context):
    # getting query
    logging.info(event)
    logging.info(context)
    query = json.loads(event['body'])
    url = query['url']
    logging.info('spreadsheet URL: {}'.format(url))

    # getting environment variables
    s3_bucket_name = os.environ.get('S3_BUCKET')
    service_account_file = os.environ.get('SERVICE_ACCOUNT_FILE')

    # get service account info
    s3_client = boto3.client('s3')
    s3_client.download_file(
        s3_bucket_name,
        service_account_file,
        os.path.join('/', 'tmp', service_account_filename)
    )
    service_account_info = json.load(open(os.path.join('/', 'tmp', service_account_filename), 'r'))

    # handling Google spreadsheet
    spreadsheet = get_google_spreadsheet_from_service_account(service_account_info, url)
    monthly_summary_dict = generate_summary_dict(spreadsheet)
    summary_df = generate_summary_df(monthly_summary_dict)
    update_summary_googlespreadsheet(
        url,
        summary_df,
        service_account_file=os.path.join('/', 'tmp', service_account_filename)
    )

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'body': json.dumps({
            'url': url,
            'summary': monthly_summary_dict
        })
    }

