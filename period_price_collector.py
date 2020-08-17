import FinanceDataReader as fdr
import pandas as pd
from tqdm import tqdm
pd.set_option('display.max_columns', 50)

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


'''daily_price'''
def daily_price_download(market ,start_date, end_date):
    code = company_info_download(market)
    # cpinfo = pd.read_csv("company_info.csv")
    # code = cpinfo['code']
    daily_price = []

    for cd in tqdm(code):
        tmp = fdr.DataReader(cd, start_date, end_date)
        # insert code column
        tmp.insert(0, 'code', cd)
        daily_price.append(tmp)

    daily_price = pd.concat(daily_price)
    # drop 'Change' column
    daily_price.drop(columns=['Change'], axis=1, inplace=True)
    # 'Date' index to column
    daily_price.reset_index(inplace=True)
    daily_price.rename(columns={'index':'Date'}, inplace=True)

    # daily_price[['Open','High','Low', 'Close', 'Volume']].astype(int)
    print(f'daily_price shape:{daily_price.shape}')
    # daily_price.to_csv("daily_price.csv", index=False)
    daily_price.to_json("daily_price_record.json", orient='records')
    print("daily_price Download complete.")



if __name__ == "__main__":
    daily_price_download('KRX', '2019-01-01', '2019-01-02')



