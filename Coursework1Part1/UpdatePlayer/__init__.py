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
    
    error_message = "a"
    result = True
    player = req.get_json()
    user_list = list(container.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  player["username"] + "\"", enable_cross_partition_query=True))
    if len(user_list) > 0:
        selected_User = user_list[0]
        updatedGamesPlayed = selected_User["games_played"]
        updatedScore = selected_User["total_score"]

    if len(user_list) == 0:
        error_message = "user does not exist"
        result = False
    elif(player["password"] != selected_User["password"]):
        error_message = "wrong password"
        result = False
    else:
        if("add_to_games_played" in player.keys()):
            if(player["add_to_games_played"] <=0 ):
                error_message = "Value to add is <=0"
                result = False
            else:
                updatedGamesPlayed = selected_User["games_played"] + player["add_to_games_played"]
        if("add_to_score" in player.keys()):
            if(player["add_to_score"] <=0 ):
                error_message = "Value to add is <=0"
                result = False
            else:
                updatedScore = selected_User["total_score"] + player["add_to_score"]
        
        container.replace_item(item = selected_User["id"], body = {"username": player["username"], "password": player["password"], "games_played": updatedGamesPlayed, "total_score": updatedScore, "id": selected_User["id"]})
        if result == True:
            error_message = "OK"

    return func.HttpResponse(json.dumps({"result": result, "msg": error_message}))
