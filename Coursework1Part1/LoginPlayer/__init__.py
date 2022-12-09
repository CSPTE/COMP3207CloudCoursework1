import json
import azure.functions as func
from azure.cosmos import CosmosClient
import logging

DATABASE_NAME = "main"
CONTAINER_NAME = "players"
URL = "https://coursework1part1.documents.azure.com:443/"
KEY = "FelsmyI8uKxf72kE4q6sLYBPvHZmn5cpfSJtcBSXP6xvqyQ7XEBP6uJ2xyI6VGCjvR0mNy0T8G5lDnyENgEFZQ=="


def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    player = req.get_json()
    error_message = "a"
    result = False

    user_list = container.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  player["username"] + "\" AND c.password=\"" + player["password"] + "\" ", enable_cross_partition_query=True)
    if len(list(user_list)) > 0:
        error_message =  "OK"
        result = True
    else:
        error_message = "Username or password incorrect"
        result = False
    return func.HttpResponse(json.dumps({"result": result, "msg": error_message }))
