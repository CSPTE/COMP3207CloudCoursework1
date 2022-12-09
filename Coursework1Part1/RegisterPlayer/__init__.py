import logging
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

    player = req.get_json()
    error_message = "a"
    result = False

    if (len(player["username"]) > 16 or len(player["username"]) < 4):
        error_message = "Username less than 4 characters or more than 16 characters"
        result = False

    elif (len(player["password"]) > 24 or len(player["password"]) < 8):
        error_message = "Password less than 8 characters or more than 24 characters"
        result = False
    else:
        player_list = container.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  player["username"] + "\"", enable_cross_partition_query=True)
        if len(list(player_list)) == 0:
            container.create_item({"username" : player["username"],
                "password" : player["password"],
                "games_played" : 0,
                "total_score" : 0},
                enable_automatic_id_generation=True)
            error_message =  "OK"
            result = True
        else:
            error_message = "Username already exists"
            result = False

    return func.HttpResponse(json.dumps({"result": result, "msg": error_message }))
