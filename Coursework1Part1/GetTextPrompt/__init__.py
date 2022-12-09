from azure.cosmos import CosmosClient
import azure.functions as func
import json
import random

DATABASE_NAME = "main"
CONTAINER_PROMPTS = "prompts"
URL = "https://coursework1part1.documents.azure.com:443/"
KEY = "FelsmyI8uKxf72kE4q6sLYBPvHZmn5cpfSJtcBSXP6xvqyQ7XEBP6uJ2xyI6VGCjvR0mNy0T8G5lDnyENgEFZQ=="

def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container_prompt = database.get_container_client(CONTAINER_PROMPTS)

    input = req.get_json()
    prompt_list = list(container_prompt.query_items(query="SELECT * FROM c", enable_cross_partition_query= True))
    returned_prompts = []

    if not input["exact"]:
        for i in range(len(prompt_list)):
            if (input["word"] in prompt_list[i]["text"]):
                returned_prompts.append({"id":prompt_list[i]["id"], "text": prompt_list[i]["text"], "username": prompt_list[i]["username"]})
    else:
        for i in range(len(prompt_list)):
            words_of_text = prompt_list[i]["text"].split()
            for k in range(len(words_of_text)):
                if(input["word"] == words_of_text[k]):
                    returned_prompts.append({"id":prompt_list[i]["id"], "text": prompt_list[i]["text"], "username": prompt_list[i]["username"]})

    return func.HttpResponse(json.dumps(returned_prompts))
