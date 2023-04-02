import os
import firebase_admin
from firebase_admin import credentials, firestore
import config
from serpapi import GoogleSearch
from chat_gpt import *
from ditch_carbon import *

# Initialize firestore client
def get_firestore_client(creds_path):
    cred = credentials.Certificate(creds_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db

# Update state for a given client
def update_state(db, state, client_id):
    doc_ref = db.collection(config.client_status_collection).document(client_id)
    doc_ref.set({
        "client_id": client_id,
        "state": state
    })

def getGoogleRecommendations(q):
    params = {
    "engine": "google_shopping",
    "q": q,
    "location": "United Kingdom",
    "hl": "en",
    "gl": "us",
    "api_key": "590ae3460ef76094aeefe6521f09436d9e78b40dd1da1fd1e0d7ff6ee466fd6c"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    related_shopping_results = results["shopping_results"]

    return related_shopping_results[0:5]


def getRecommendations(product):

    recommended_products = []
    recommendations = getGoogleRecommendations(product)
    titles = [i["title"] for i in recommendations]
    titels_prices = []

    for i in recommendations:
        recom = []

        recom.append(i["title"])
        recom.append(i["price"])
        recom.append(i["link"])
        recom.append(i["thumbnail"])

        if "rating" in i:
            recom.append(i["rating"])
        else:
            recom.append(None)

        if "reviews" in i:
            recom.append(i["reviews"])
        else:
            recom.append(None)

        titels_prices.append(recom)
        

    extracted_titles = extractInfoMultiple(titles)
    extracted_titles = [i for i in extracted_titles if len(i)>0]

    for idx, t in enumerate(extracted_titles):
        price = titels_prices[idx][1]
        link = titels_prices[idx][2]
        thumbnail = titels_prices[idx][3]
        rating = titels_prices[idx][4]
        reviews = titels_prices[idx][5]
        
        rec_product = t.strip().split(",")[0].strip()
        rec_manufacturer = t.strip().split(",")[1]


        rec_product_co2 = getCarbonData(rec_product, rec_manufacturer)
        rec_manu_co2 = getCarbonDataManu(rec_manufacturer)


        recommended_products.append({"product": rec_product, 
                                     "manu": rec_manufacturer, 
                                     "product_co2": rec_product_co2, 
                                     "price": price,
                                     "link": link,
                                     "rating":rating,
                                     "reviews":reviews,
                                     "thumbnail":thumbnail,
                                     "rec_manu_co2": rec_manu_co2})


    return recommended_products


getRecommendations("Monster Energy Ultra Rosa")