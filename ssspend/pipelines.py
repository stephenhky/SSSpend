
from collections import defaultdict

from tqdm import tqdm

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


# Or use pandas?
def generate_summary_df(monthly_summary_dict):
    yearly_summary_dict = defaultdict(lambda : 0)
    for monthly_summary in monthly_summary_dict.values():
        for category, amount in monthly_summary:
            yearly_summary_dict[category] += amount
