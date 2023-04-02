import requests
import json

#Param url: https://www.amazon.co.uk/Oral-B-Toothbrush/dp/B08TMSQ2R7
#Return: B08TMSQ2R7
def getasin(url):
    dp_start = url.find("/dp/")
    url = url[dp_start+4:]
    asin_end = url.find("/")
    asin = url[:asin_end]
    return asin

# Takes in an asin for amazon and returns an array of data from the amazon page.
# Param: asin
# Return: [Rating, Array of products(title, rating, price)].
# Warning: Rating may be None and/or array of products may not exist.
def getRecommendations(productID):
    params = {
        'api_key': '47F7D551BEA44E3EB84FA4BFF3FA81F6',
        'amazon_domain': 'amazon.co.uk',
        'asin': str(productID),
        'type': 'product'
    }
    result = requests.get('https://api.rainforestapi.com/request', params).json()
    finalResult = [None]
    if 'product' in result and 'rating' in result['product']:
        finalResult = [result['product']['rating']]
    try:
        if 'also_viewed' in result:
            for i in result['also_viewed']:
                finalResult.append((i['title'], i['rating'], i['price']['raw']))
        elif 'also_bought' in result:
            for i in result['also_bought']:
                finalResult.append((i['title'], i['rating'], i['price']['raw']))
        elif 'frequently_bought_together' in result:
            for i in result['frequently_bought_together']['products']:
                finalResult.append((i['title'], i['price']['raw']))
        else:
            finalResult.append(False)

    except KeyError:
        finalResult.append(False)
    finally:
        return finalResult

