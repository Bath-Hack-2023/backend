from flask import Flask, request, jsonify
from flask_cors import CORS
from ditch_carbon import *
from html_parser import *
from chat_gpt import *
from util import *
import config


app = Flask(__name__)
cors = CORS(app)

# Connect to firebase and update state
db = get_firestore_client(config.firebase_creds)



@app.route('/post/item', methods=['POST'])
def get_url():
    try:
        # Extract data from request
        data = request.get_json()
        url = data['url']
        client_id = data['client_id']

        # Get the item title
        update_state(db, "Parsing HTML", client_id)
        product_title, error = getProductTitle(url)
        
        # Check if there was an error getting title
        if error != None:
            print(error)
            update_state(db, f"Error occured: {error}", client_id)
            return jsonify({"error": f"Error occured while parsing html: {error}", "data": None}), 200
        
        # Use chat gpt to extract product name and company
        update_state(db, "Extracting product information", client_id)
        product_info = extractInfoOne(product_title)

        if product_info == None:
            update_state(db, f"Error while extracting product information", client_id)
            return jsonify({"error": f"Error while extracting product information", "data": None}), 200
        
        product_name = product_info[0].strip()
        manufacturer = product_info[1].strip()

        update_state(db, "Getting Carbon Data", client_id)

        # Get Carbon data
        carbon_data = getCarbonData(product_name, manufacturer)
        manu_carbon_data = getCarbonDataManu(manufacturer)

        # Update state for client
        update_state(db, "Sending data", client_id)

        data = {"product_title": product_title, 
                "product_name": product_name, 
                "manufacturer": manufacturer,
                "carbon_data": carbon_data,
                "manu_carbon_data": manu_carbon_data
                }
        
        print(data)

        # Respond
        return jsonify({"error": None, "data": data}), 200

    except Exception as e:
        print(e)
        update_state(db, f"Error occured: {e}", client_id)
        return jsonify({"error": f"Ooops something went wrong: {e}", "data": None}), 400
    
@app.route('/post/recommendations', methods=['POST'])
def get_recommended():
    try:
        # Extract data from request
        data = request.get_json()
        url = data['url']

        # Get the item title
        product_title, error = getProductTitle(url)
        
        # Check if there was an error getting title
        if error != None:
            print(error)
            return jsonify({"error": f"Error occured while parsing html: {error}", "data": None}), 200
        
        # Use chat gpt to extract product name and company
        product_info = extractInfoOne(product_title)

        if product_info == None:
            return jsonify({"error": f"Error while extracting product information", "data": None}), 200
        
        product_name = product_info[0].strip()

        try:
            recommended_products = getRecommendations(product_name)
        except Exception as e:
            recommended_products = []

        data = {"recommended": recommended_products}

        # Respond
        return jsonify({"error": None, "data": data}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"Ooops something went wrong: {e}", "data": None}), 400



    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.http_port, ssl_context=config.ssl_context)

