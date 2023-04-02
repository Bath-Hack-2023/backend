import requests
from chat_gpt import getCarbonInfoOne, getCarbonInfoManuGPT
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
    if "error" in response:
        return getCarbonInfoManuGPT(manu)
    answer = ""
    if "emissions" in response:
        if "total_kg_co2" in response["emissions"]:
            return  response["emissions"]["total_kg_co2"]
    if "ef_kg_co2eq" in response:
        return response["ef_kg_co2eq"]

