import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import html_parser
import config
from html_parser import *
from util import *
import time

app = Flask(__name__)
cors = CORS(app)


@app.route('/post/item', methods=['POST'])
def get_url():
    try:
        # Extract data from request
        data = request.get_json()
        url = data['url']
        client_id = data['client_id']

        # Connect to firebase and update state
        db = get_firestore_client(config.firebase_creds)
        update_state(db, "Parsing HTML", client_id)

        # Get the item title
        product_title, error = getProductTitle(url)
        
        # Check if there was an error getting title
        if error != None:
            print(error)
            update_state(db, f"Error occured: {error}", client_id)
            return jsonify({"error": f"Error occured while parsing html: {error}", "data": None}), 200
        
        # Update state for client
        update_state(db, "Sending data", client_id)

        # Respond
        return jsonify({"error": None, "data":{"product_title": product_title}}), 200

    except Exception as e:
        print(e)
        update_state(db, f"Error occured: {error}", client_id)
        return jsonify({"error": f"Ooops something went wrong: {e}", "data": None}), 400


    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.http_port, debug=True)

