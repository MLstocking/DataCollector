from azure.cosmos import CosmosClient
import pandas as pd
import json

config = {
    "endpoint": "",
    "primarykey": ""
}
client = CosmosClient(config["endpoint"], config["primarykey"])

database_name = 'MLStocking'
database = client.get_database_client(database_name)
container_name = 'daily_price'
container = database.get_container_client(container_name)

# Get the number of items in daily_price container
continued_items = container.query_items(
    query='SELECT VALUE COUNT(1) FROM daily_price',
    enable_cross_partition_query=True)

for item in continued_items:
    records_cnt = json.dumps(item, indent=True)

item_cnt = int(records_cnt)

# Download and read csv file
df = pd.read_csv('period_price.csv')

# Cosmos DB needs one column named 'id'.
new_id = [x for x in range(item_cnt, item_cnt+len(df))]
df['id'] = new_id

# Convert the id column to a string - this is a document database.
df['id'] = df['id'].astype(str)

# Write rows of a pandas DataFrame as items to the Database Container
for i in range(0,df.shape[0]):
    # create a dictionary for the selected row
    data_dict = dict(df.iloc[i,:])
    # convert the dictionary to a json object.
    data_dict = json.dumps(data_dict)
    insert_data = container.upsert_item(json.loads(data_dict))

print('Records inserted successfully.')

