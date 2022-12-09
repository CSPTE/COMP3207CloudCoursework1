import json
import azure.functions as func
from azure.cosmos import CosmosClient

DATABASE_NAME = "main"
CONTAINER_NAME = "players"
URL = "https://coursework1part1.documents.azure.com:443/"
KEY = "FelsmyI8uKxf72kE4q6sLYBPvHZmn5cpfSJtcBSXP6xvqyQ7XEBP6uJ2xyI6VGCjvR0mNy0T8G5lDnyENgEFZQ=="


def main(req: func.HttpRequest) -> func.HttpResponse:
    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    number = req.get_json()["top"]  
    output = list(container.query_items(query="SELECT p.username, p.total_score AS score, p.games_played FROM player p ORDER BY p.total_score DESC, p.username ASC OFFSET 0 LIMIT " + str(number), enable_cross_partition_query=True))

    return func.HttpResponse(json.dumps(output))