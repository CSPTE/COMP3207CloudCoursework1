from azure.cosmos import CosmosClient
import azure.functions as func
import json
import random

DATABASE_NAME = "main"
CONTAINER_PLAYERS = "players"
CONTAINER_PROMPTS = "prompts"
URL = "https://coursework1part1.documents.azure.com:443/"
KEY = "FelsmyI8uKxf72kE4q6sLYBPvHZmn5cpfSJtcBSXP6xvqyQ7XEBP6uJ2xyI6VGCjvR0mNy0T8G5lDnyENgEFZQ=="

def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container_prompt = database.get_container_client(CONTAINER_PROMPTS)

    prompt_list = list(container_prompt.query_items(query = "SELECT * FROM c", enable_cross_partition_query= True))
    returned_prompts = []
    input = req.get_json()

    if("prompts" in input.keys()):
        if(len(prompt_list) <= input["prompts"]):
            for i in range (len(prompt_list)):
                returned_prompts.append({"id": prompt_list[i]["id"], "text": prompt_list[i]["text"], "username": prompt_list[i]["username"]})
        else:
            random_numbers = random.sample(range(0, len(prompt_list)), input["prompts"])
            for i in range(input["prompts"]):
                returned_prompts.append({"id": prompt_list[random_numbers[i]]["id"], "text": prompt_list[random_numbers[i]]["text"], "username": prompt_list[random_numbers[i]]["username"]})
    else:
        usernames = input["players"]
        for i in range(len(usernames)):
            to_append = list(container_prompt.query_items(query = 
                "SELECT * FROM c WHERE c.username=\"" + usernames[i] + "\"", enable_cross_partition_query=True))

            if(len(to_append) != 0):
                for k in range(len(to_append)):
                    returned_prompts.append({"id": to_append[k]["id"], "text": to_append[k]["text"], "username": to_append[k]["username"]})

    return func.HttpResponse(json.dumps(returned_prompts))
