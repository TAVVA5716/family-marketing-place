from pymongo import MongoClient
from datetime import datetime

def test_mongodb_connection():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ecommerce']
        
        # Test write operation
        test_user = {
            'username': 'test_user',
            'email': 'test@example.com',
            'created_at': datetime.now()
        }
        users = db.users
        user_id = users.insert_one(test_user).inserted_id
        print("✓ Successfully wrote test user to database")
        
        # Test read operation
        found_user = users.find_one({'_id': user_id})
        if found_user:
            print("✓ Successfully read test user from database")
            print(f"Found user: {found_user['username']}")
        
        # Show all collections
        print("\nExisting collections:")
        collections = db.list_collection_names()
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"- {collection}: {count} documents")
        
        # Show sample data from each collection
        print("\nSample data from collections:")
        for collection in collections:
            print(f"\n{collection} collection:")
            for doc in db[collection].find().limit(2):
                print(doc)
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing MongoDB connection and operations...")
    test_mongodb_connection()
