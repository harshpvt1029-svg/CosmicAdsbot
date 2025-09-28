import pymongo
import os
from crypto_utils import encrypt_session, decrypt_session

MONGO_URI = os.getenv("mongodb+srv://nehraharsh553_db_user:c6HZPt33bIUeOruK@cosmic.tqngm4y.mongodb.net/?retryWrites=true&w=majority&appName=Cosmic")
client = pymongo.MongoClient(MONGO_URI)
db = client["auto_ad_bot"]

# ------------------ USERS ------------------
def add_user(user_id):
    """Add a new user to DB"""
    db.users.insert_one({
        "user_id": user_id,
        "premium": False,
        "policy_accepted": False,   # Track if privacy accepted
        "policy_version": 1
    })

def get_user(user_id):
    """Get user info"""
    return db.users.find_one({"user_id": user_id})

def set_policy_accepted(user_id):
    """Mark user accepted privacy policy"""
    db.users.update_one({"user_id": user_id}, {"$set": {"policy_accepted": True}})

def set_premium(user_id, value=True):
    """Mark user as premium"""
    db.users.update_one({"user_id": user_id}, {"$set": {"premium": value}})

# ------------------ ACCOUNTS ------------------
def save_account(user_id, session_string):
    """Save user account (encrypted)"""
    db.accounts.insert_one({
        "user_id": user_id,
        "session": encrypt_session(session_string)
    })

def get_accounts(user_id):
    """Return decrypted accounts for a user"""
    accounts = db.accounts.find({"user_id": user_id})
    return [decrypt_session(a["session"]) for a in accounts]

def remove_account(user_id, session_string):
    """Remove account from DB"""
    db.accounts.delete_one({"user_id": user_id, "session": encrypt_session(session_string)})

# ------------------ LOGS ------------------
def log_message(account_username, group_id, message_id, status):
    """Save message logs"""
    db.logs.insert_one({
        "account": account_username,
        "group_id": group_id,
        "message_id": message_id,
        "status": status
    })

def get_logs(limit=50):
    """Return last N logs"""
    return list(db.logs.find().sort("_id", -1).limit(limit))

# ------------------ APPROVED USERS ------------------
def approve_user(username, admin_username):
    """Mark user as approved by admin"""
    db.approved.insert_one({
        "username": username,
        "approved_by": admin_username
    })

def is_approved(username):
    """Check if user is approved"""
    return db.approved.find_one({"username": username}) is not None

# ------------------ PREMIUM USERS ------------------
def get_premium_users():
    """Return all premium users"""
    return list(db.users.find({"premium": True}))
