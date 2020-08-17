import FinanceDataReader as fdr
import pandas as pd
from tqdm import tqdm

'''company_info'''
def company_info_download(market):
    if market not in ['KRX', 'KOSPI', 'KOSDAG', 'KONEX']:
        print("Invalid input value.")
    company_info = fdr.StockListing(market)
    company_info = company_info[['Symbol', 'Name']]
    company_info.rename(columns={'Symbol':'code', 'Name':'company'},inplace=True)

    # duplicate code(symbol) check
    if company_info.duplicated(['code']).sum() > 0:
        print("Duplicate value exists.")

    print(f'company_info shape:{company_info.shape}')
    company_info.to_csv("company_info.csv", index=False)
    print("company_info Download complete.")
    return company_info['code'].tolist()


'''period_price'''
def period_price_download(market ,start_date, end_date):
    code = company_info_download(market)
    period_price = []

    for cd in tqdm(code):
        tmp = fdr.DataReader(cd, start_date, end_date)
        # insert code column
        tmp.insert(0, 'code', cd)
        period_price.append(tmp)

    period_price = pd.concat(period_price)
    # drop 'Change' column
    period_price.drop(columns=['Change'], axis=1, inplace=True)
    # 'Date' index to column
    period_price.reset_index(inplace=True)
    period_price.rename(columns={'index':'Date'}, inplace=True)

    # daily_price[['Open','High','Low', 'Close', 'Volume']].astype(int)
    print(f'daily_price shape:{period_price.shape}')
    period_price.to_csv("period_price"+start_date+'_'+end_date+".csv", index=False)

    print("period_price Download complete.")



if __name__ == "__main__":
    period_price_download('KRX', '2019-01-01', '2019-01-02')

