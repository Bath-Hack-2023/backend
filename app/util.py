import os
import firebase_admin
from firebase_admin import credentials, firestore
import config

# Initialize firestore client
def get_firestore_client(creds_path):
    cred = credentials.Certificate(creds_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db

# Update state for a given client
def update_state(db, state, client_id):
    doc_ref = db.collection(config.client_status_collection).document(config.client_status_document)
    doc_ref.set({
        f'{client_id}': state
    })


db = get_firestore_client(config.firebase_creds)
update_state(db, "TEST_STATE", "TEST_ID")

