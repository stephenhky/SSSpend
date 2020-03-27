
from tqdm import tqdm
import pandas as pd

from .knowledge import months
from .spenddataframe import get_month_dataframe
from .utils import category_preprocessor


def generate_summary_dict(spreadsheet, category_preprocessor=category_preprocessor):
    monthly_summary_dict = {month: {} for month in months}
    for month in tqdm(months):
        df = get_month_dataframe(spreadsheet, month)
        sumdf = df[['Category', 'Debit']].groupby('Category', as_index=False).agg({'Debit': 'sum'})
        sumdf['Category'] = sumdf['Category'].apply(category_preprocessor)
        monthly_summary_dict[month] = {category: sum
                                       for category, sum in zip(sumdf['Category'], sumdf['Debit'])}

    return monthly_summary_dict


def generate_summary_df(monthly_summary_dict):
    summary_df = pd.DataFrame.from_dict(monthly_summary_dict).fillna(0)
    summary_df['Total'] = summary_df.apply(lambda row: sum([row[month] for month in months]),
                                           axis=1)
    summary_df = summary_df.sort_values(by='Total', ascending=False)
    return summary_df
