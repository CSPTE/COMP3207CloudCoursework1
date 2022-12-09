from azure.cosmos import CosmosClient
import azure.functions as func
import json

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
    user_list = list(container_users.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  prompt ["username"] + "\" AND c.password=\"" + prompt["password"] + "\" ", enable_cross_partition_query=True))
    user_prompts = list(container_prompt.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  prompt ["username"] + "\"", enable_cross_partition_query=True))
    prompt_Already_Exist = False
    user_id = list(container_prompt.query_items(query = "SELECT * FROM c WHERE c.id=\"" +  str(prompt["id"]) + "\"", enable_cross_partition_query= True))

    for prompts in user_prompts:
            if (prompts["text"] == prompt["text"]):
                prompt_Already_Exist = True

    if len(user_list) == 0:
        error_message = "bad username or password"
        result = False
    elif (len(prompt["text"]) < 20 or len(prompt["text"]) > 100):
        error_message = "prompt length is <20 or > 100 characters"
        result = False
    elif (prompt_Already_Exist):
        error_message = "This user already has a prompt with the same text"
        result = False
    elif(len(user_id) == 0):
        error_message = "prompt id does not exist"
        result = False
    else:
        container_prompt.replace_item(item = str(prompt["id"]), body = {"text": prompt["text"], "username": prompt ["username"], "id": str(prompt["id"])})
        if result == True:
            error_message = "OK"

    return func.HttpResponse(json.dumps({"result": result, "msg": error_message}))