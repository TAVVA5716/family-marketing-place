from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt
from datetime import datetime

# Load environment variables
load_dotenv()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def init_sample_data():
    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
    db = client['ecommerce']
    
    # Clear existing collections
    db.products.delete_many({})
    db.users.delete_many({})
    
    # Create admin user
    admin_exists = db.users.find_one({'role': 'admin'})
    if not admin_exists:
        admin_user = {
            'username': 'admin',
            'password': hash_password('admin123'),
            'email': 'admin@example.com',
            'role': 'admin',
            'created_at': datetime.now()
        }
        db.users.insert_one(admin_user)
        print("Admin user created - username: admin, password: admin123")
    
    # Sample products
    products = [
        {
            'name': 'Laptop',
            'price': 999.99,
            'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
            'image_path': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400',
            'seller_id': 'sample'
        },
        {
            'name': 'Smartphone',
            'price': 699.99,
            'description': 'Latest smartphone with 5G capability',
            'image_path': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
            'seller_id': 'sample'
        },
        {
            'name': 'Headphones',
            'price': 199.99,
            'description': 'Wireless noise-canceling headphones',
            'image_path': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            'seller_id': 'sample'
        },
        {
            'name': 'Smartwatch',
            'price': 299.99,
            'description': 'Fitness tracking smartwatch',
            'image_path': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
            'seller_id': 'sample'
        },
        {
            'name': 'Tablet',
            'price': 449.99,
            'description': '10-inch tablet with retina display',
            'image_path': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400',
            'seller_id': 'sample'
        },
        {
            'name': 'Camera',
            'price': 799.99,
            'description': 'Digital camera with 4K video',
            'image_path': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400',
            'seller_id': 'sample'
        }
    ]
    
    # Insert products
    db.products.insert_many(products)
    print("Sample data initialized successfully!")

if __name__ == "__main__":
    init_sample_data()
