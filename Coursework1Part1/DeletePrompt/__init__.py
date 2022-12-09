import logging
from azure.cosmos import CosmosClient
import azure.functions as func
import json
import uuid

DATABASE_NAME = "main"
CONTAINER_PLAYERS = "players"
CONTAINER_PROMPTS = "prompts"
URL = "https://coursework1part1.documents.azure.com:443/"
KEY = "FelsmyI8uKxf72kE4q6sLYBPvHZmn5cpfSJtcBSXP6xvqyQ7XEBP6uJ2xyI6VGCjvR0mNy0T8G5lDnyENgEFZQ=="

def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container_users = database.get_container_client(CONTAINER_PLAYERS)
    container_prompt = database.get_container_client(CONTAINER_PROMPTS)

    prompt = req.get_json()
    error_message = "a"
    result = True

    user_list = list(container_users.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  prompt["username"] + "\" AND c.password=\"" + prompt["password"] + "\" ", enable_cross_partition_query=True))
    user_id = list(container_prompt.query_items(query = "SELECT c.username FROM c WHERE c.id=\"" +  str(prompt["id"]) + "\"", enable_cross_partition_query= True))

    if len(user_list) == 0:
        error_message = "bad username or password"
        result = False
    elif(len(user_id) == 0):
        error_message = "prompt id does not exist"
        result = False
    elif(user_id[0]["username"] != prompt["username"]):
        error_message = "access denied"
        result = False
    else:
        container_prompt.delete_item(item = str(prompt["id"]), partition_key=str(prompt["id"]))
        error_message = "OK"
        result = True

    return func.HttpResponse(json.dumps({"result": result, "msg": error_message}))
