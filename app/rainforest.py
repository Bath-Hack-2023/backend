import requests
import json

# set up the request parameters
params = {
'api_key': '47F7D551BEA44E3EB84FA4BFF3FA81F6',
  'amazon_domain': 'amazon.co.uk',
  'asin': 'B073JYC4XM',
  'type': 'product'
}

# make the http GET request to Rainforest API
api_result = requests.get('https://api.rainforestapi.com/request', params)

# print the JSON response from Rainforest API
print(json.dumps(api_result.json()))

def getRecomendation():
  pass