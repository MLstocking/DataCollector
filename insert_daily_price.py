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

# Download and read csv file
df = pd.read_csv('daily_price.csv')
# Reset index - creates a column called 'index'
df = df.reset_index()
# Cosmos DB needs one column named 'id'.
df = df.rename(columns={'index':'id'})
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

