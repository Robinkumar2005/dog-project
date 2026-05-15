import requests
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("DOG_API")

def get_breed_info(breed_name):

    url = f"https://api.thedogapi.com/v1/breeds/search?q={breed_name}"

    auth_headers = {
    "x-api-key": api_key
}

    response = requests.get(url, headers=auth_headers)
    if response.status_code != 200:
        print(f"Error fetching breed info: {response.status_code}")
        return None
    data = response.json()

    if len(data) > 0:

        dog = data[0]

        result = {
            "name": dog.get("name"),
            "life_span": dog.get("life_span"),
            "temperament": dog.get("temperament"),
            "origin": dog.get("origin"),
            "description": dog.get("description"),
            "history": dog.get("breed_group"),
            "weight": dog.get("weight", {}).get("metric"),
            "height": dog.get("height", {}).get("metric")
        }

        return result

    else:
        print("Breed not found")
        return None

