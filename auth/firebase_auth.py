# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, auth
# import json
# from typing import Optional, Dict
# import datetime

# class FirebaseAuth:
#     def __init__(self, config: Dict):
#         self.firebase = pyrebase.initialize_app(config)
#         self.auth = self.firebase.auth()
#         self.db = self.firebase.database()
        
#     def sign_up(self, email: str, password: str, username: str) -> bool:
#         try:
#             user = self.auth.create_user_with_email_and_password(email, password)
#             # Store user info in database
#             self.db.child("users").child(user['localId']).set({
#                 "username": username,
#                 "email": email,
#                 "created_at": str(datetime.now())
#             })
#             return True
#         except Exception as e:
#             st.error(f"Sign up failed: {e}")
#             return False
            
#     def sign_in(self, email: str, password: str) -> Optional[Dict]:
#         try:
#             user = self.auth.sign_in_with_email_and_password(email, password)
#             return user
#         except Exception as e:
#             st.error(f"Sign in failed: {e}")
#             return None



import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
from typing import Optional, Dict
import datetime

class FirebaseAuth:
    def __init__(self, config: Dict):
        # Initialize the Firebase Admin SDK
        if not firebase_admin._apps:
            cred = credentials.Certificate(config)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        
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
