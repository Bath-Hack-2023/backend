import os

vendor_title_ids = {
    "amazon": "#productTitle"
}

client_status_collection = "client_states"
client_status_document = "states"
firebase_creds = os.environ["FIREBASE_CREDS"]
open_ai_creds = os.environ["CHATGPT_API_KEY"]
carbon_api_creds = os.environ["CARBON_API"]
google_search_creds = os.environ["GOOGLE_SEARCH_KEY"]

http_port = 6969

SSL_CERT = os.environ["SSL_CERT"]
SSL_KEY = os.environ["SSL_KEY"]

ssl_context = (SSL_CERT, SSL_KEY)