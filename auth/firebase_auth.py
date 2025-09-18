import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
from typing import Optional, Dict
import datetime

class FirebaseAuth:
    def __init__(self, config: Dict):
        # Initialize the Firebase Admin SDK
        # if not firebase_admin._apps:
        #     cred = credentials.Certificate(config)
        #     firebase_admin.initialize_app(cred)
        # self.db = firestore.client()
        #if not firebase_admin._apps:
        if not firebase_admin._apps:
                try:
                    # Use service account info from Streamlit secrets
                    cred = credentials.Certificate(config)
                    firebase_admin.initialize_app(cred)
                except Exception as e:
                    st.error(f"Firebase initialization failed: {e}")
                    raise e
        
    def sign_up(self, email: str, password: str, username: str) -> bool:
        try:
            # Create a new user with email and password
            user_record = auth.create_user(email=email, password=password, display_name=username)
            # Store user info in Firestore
            self.db.collection("users").document(user_record.uid).set({
                "username": username,
                "email": email,
                "created_at": datetime.datetime.now().isoformat()
            })
            return True
        except Exception as e:
            st.error(f"Sign up failed: {e}")
            return False
            
    def sign_in(self, email: str, password: str) -> Optional[Dict]:
        try:
            # Sign in with email and password
            user = auth.get_user_by_email(email)
            return {'localId': user.uid, 'email': user.email}
        except Exception as e:
            st.error(f"Sign in failed: {e}")
            return None
