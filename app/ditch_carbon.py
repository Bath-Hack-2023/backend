import requests
from chat_gpt import getCarbonInfoOne, getCarbonInfoMultiple
import json


def getCarbonData(product, manufacturer):
    url = f"https://api.ditchcarbon.com/v1.0/product?name={product}&manufacturer={manufacturer}"
    headers = {"accept": "application/json", "Authorization": "Bearer 92d3af4ac158430ec82fd01adf0093de"}
    response = (requests.get(url, headers=headers)).json()
    if "errors" in response:

        # TODO: Handle error with chatgpt
        return getCarbonInfoOne(product, manufacturer)
    return response["carbon_footprint"]


# Param: product array from rainforest.
# Return: Array of CO2s
# Return array may contain -1 values, representing 'could not find data'
def getCarbonDataMultiple(array):
    result = []
    fetch = []
    for product in array:
        print(product)
        if product != '':
            product = product.split(",")
            url = f"https://api.ditchcarbon.com/v1.0/product?name={product[0]}&manufacturer={product[1]}"
            headers = {"accept": "application/json", "Authorization": "Bearer 92d3af4ac158430ec82fd01adf0093de"}
            response = (requests.get(url, headers=headers)).json()
            if "errors" in response:
                print("ditch carbon had a problem")
                result.append(-1)
                fetch.append(product)
            else:
                result.append(response["carbon_footprint"])
        else:
            print("couldn't process")
            result.append(-1)
            fetch.append(product)

    if fetch != []:
        fetch = getCarbonInfoMultiple(fetch)
        print(fetch)
        print(result)
        if fetch != None:
            j = 0
            for i in range(len(result)):
                if j >= len(fetch):
                    break
                if result[i] == -1:
                    if fetch[j] == None:
                        result[i] = fetch[j]
                    j+=1
    return result

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

