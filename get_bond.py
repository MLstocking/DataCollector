import investpy
import json
import sys
from azure.cosmos import CosmosClient


def get_bond(argv):
    start = argv[0]
    end = argv[1]

    df = investpy.get_bond_historical_data(bond='South Korea 10Y', from_date=start, to_date=end)
    df.reset_index(level=0, inplace=True)
    df = df[['Date', 'Close']]
    return df


def insert_fs(df):
    for col in df.columns:
        df[col] = df[col].astype(str)

    config = {
        "endpoint": "",
        "primarykey": ""
    }

    client = CosmosClient(config["endpoint"], config["primarykey"])

    database_name = 'MLStocking'
    database = client.get_database_client(database_name)
    container_name = 'bond'
    container = database.get_container_client(container_name)

    # Get the number of items in daily_price container
    continued_items = container.query_items(
        query='SELECT VALUE COUNT(1) FROM financial_statement',
        enable_cross_partition_query=True)

    for item in continued_items:
        records_cnt = json.dumps(item, indent=True)

    item_cnt = int(records_cnt)

    # Cosmos DB needs one column named 'id'.
    new_id = [x for x in range(item_cnt, item_cnt + len(df))]
    df['id'] = new_id

    # Convert the id column to a string - this is a document database.
    df['id'] = df['id'].astype(str)

    # Write rows of a pandas DataFrame as items to the Database Container
    for i in range(0, df.shape[0]):
        # create a dictionary for the selected row
        data_dict = dict(df.iloc[i, :])
        # convert the dictionary to a json object.
        data_dict = json.dumps(data_dict)
        container.upsert_item(json.loads(data_dict))

    print('Records inserted successfully.')


if __name__ == "__main__":
    #bond = get_bond('01/01/2010', '01/10/2020')
    bond = get_bond(sys.argv[1:])
    insert_fs(bond)
