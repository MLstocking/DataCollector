from azure.cosmos import CosmosClient
import pandas as pd
import json

config = {
    "endpoint": "https://jang.documents.azure.com:443/",
    "primarykey": "xD4e14e4B9hHFCnqwuTqIz9CkKU3APSU5Wcj9KD0tsWaphFBwTYLY9Wr97ks0Q0PBcRfbaqUA9kreBKAMS81nQ=="
}
client = CosmosClient(config["endpoint"], config["primarykey"])

database_name = 'testDatabase'
database = client.get_database_client(database_name)
container_name = 'testContainer'
container = database.get_container_client(container_name)

# Download and read csv file
df = pd.read_csv('company_info.csv')
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
