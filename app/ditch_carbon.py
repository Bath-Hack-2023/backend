import requests
from chat_gpt import getCarbonInfoOne
import json


def getCarbonData(product, manufacturer):
    url = f"https://api.ditchcarbon.com/v1.0/product?name={product}&manufacturer={manufacturer}"
    headers = {"accept": "application/json", "Authorization": "Bearer 92d3af4ac158430ec82fd01adf0093de"}
    response = (requests.get(url, headers=headers)).json()
    if "errors" in response:

        # TODO: Handle error with chatgpt
        return getCarbonInfoOne(product, manufacturer)
    return response["carbon_footprint"]


# Get carbon emissions data for manufacturers
# Param: manufacturer name
# Return: Carbon emissions data
def getCarbonDataManu(manu):
    url = f"https://api.ditchcarbon.com/v1.0/supplier?name={manu}"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer 92d3af4ac158430ec82fd01adf0093de"
    }

    response = requests.get(url, headers=headers).json()
    if "errors" in response:
        response = getCarbonDataManu(manu)
        if response is not None:
            return response
        return None
    return response["emissions"]["total_kg_co2"]

