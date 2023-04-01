import requests
import json

def getCarbonData(product, manufacturer):
    url = f"https://api.ditchcarbon.com/v1.0/product?name={product}&manufacturer={manufacturer}"
    headers = {"accept": "application/json", "Authorization": "Bearer 92d3af4ac158430ec82fd01adf0093de"}
    response = (requests.get(url, headers=headers)).json()
    if "errors" in response:
        #TODO: Handle error with chatgpt
        print("This is an error")
    else:
        print(response)
        return response["carbon_footprint"]
        
