from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Create the cosmos client
config = {
    "endpoint": "",
    "primarykey": ""
}
client = CosmosClient(config["endpoint"], config["primarykey"])

# Create database
database_name = 'testDatabase'
try:
    database = client.create_database(database_name)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(database_name)

# Create Container
container_name = 'testContainer'
try:
    container = database.create_container(id=container_name, partition_key=PartitionKey(path="/country"))
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(container_name)
except exceptions.CosmosHttpResponseError:
    raise

database_client = client.get_database_client(database_name)
container_client = database.get_container_client(container_name)
