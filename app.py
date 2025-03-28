import streamlit as st
import bcrypt
from PIL import Image
import os
from dotenv import load_dotenv
import stripe
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# Load environment variables
load_dotenv()

# Initialize MongoDB
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['ecommerce']

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Custom CSS
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        /* Main Container */
        .main {
            font-family: 'Poppins', sans-serif;
            padding: 2rem;
        }

        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #6DD5FA, #2980B9);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        /* Product Card Styles */
        .product-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }

        .product-card img {
            border-radius: 8px;
            margin-bottom: 1rem;
        }

        .product-card h3 {
            color: #2C3E50;
            margin-bottom: 0.5rem;
        }

        .product-card .price {
            color: #2980B9;
            font-size: 1.25rem;
            font-weight: 600;
        }

        /* Button Styles */
        .stButton > button {
            background-color: #2980B9;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: 500;
            transition: background-color 0.3s;
        }

        .stButton > button:hover {
            background-color: #2471A3;
        }

        /* Form Styles */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 5px;
            border: 1px solid #BDC3C7;
            padding: 0.5rem;
        }

        /* Cart Styles */
        .cart-item {
            background: #F8F9FA;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Admin Panel Styles */
        .admin-section {
            background: #ECF0F1;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }

        /* Seller Dashboard Styles */
        .seller-section {
            background: #E8F6F3;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }

        /* Status Messages */
        .success-msg {
            background: #D4EFDF;
            color: #27AE60;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }

        .error-msg {
            background: #FADBD8;
            color: #C0392B;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }

        /* Admin Dashboard Styles */
        .admin-metric {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .admin-metric h3 {
            color: #2C3E50;
            margin-bottom: 0.5rem;
        }
        
        .admin-metric .value {
            font-size: 2rem;
            font-weight: 600;
            color: #2980B9;
        }
        
        .activity-feed {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .activity-item {
            padding: 0.5rem;
            border-left: 3px solid #2980B9;
            margin-bottom: 0.5rem;
        }
        
        .admin-section {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }
        
        .admin-section:hover {
            transform: translateY(-2px);
        }
        
        /* Tab Styles */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: #F8F9FA;
            border-radius: 10px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 20px;
            color: #2C3E50;
            border-radius: 5px;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #2980B9 !important;
            color: white !important;
        }
        
        /* Filter Styles */
        .filter-section {
            background: #F8F9FA;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        /* Details/Summary Styles */
        details {
            background: #F8F9FA;
            padding: 0.5rem;
            border-radius: 5px;
            margin-top: 0.5rem;
        }
        
        summary {
            cursor: pointer;
            padding: 0.5rem;
            color: #2980B9;
        }
        
        details[open] summary {
            margin-bottom: 0.5rem;
        }
        
        /* Hero Section Styles */
        .hero-section {
            background: linear-gradient(rgba(19, 25, 33, 0.65), rgba(19, 25, 33, 0.65)),
                        url('https://images.unsplash.com/photo-1511895426328-dc8714191300?w=1200');
            background-size: cover;
            background-position: center 40%;
            text-align: center;
            padding: 5rem 2rem;
            margin: -80px -80px 2rem -80px;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(255, 153, 0, 0.2), rgba(255, 216, 20, 0.1));
            z-index: 1;
        }
        
        .hero-content {
            position: relative;
            z-index: 2;
        }
        
        .hero-title {
            font-family: 'Arial Black', sans-serif;
            font-size: 3.8rem;
            font-weight: 900;
            background: linear-gradient(45deg, #FFD814, #FF9900);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin: 0;
            padding: 0;
            text-transform: uppercase;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            line-height: 1.2;
        }
        
        .hero-subtitle {
            color: #FFD814;
            font-size: 1.6rem;
            margin-top: 1.2rem;
            font-weight: 500;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
        }

        @media (max-width: 768px) {
            .hero-section {
                margin: -40px -40px 1rem -40px;
                padding: 3rem 1rem;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.2rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

# Authentication functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(username, password, email, role='buyer'):
    users = db.users
    try:
        if users.find_one({'$or': [{'username': username}, {'email': email}]}):
            return False
        
        hashed_password = hash_password(password)
        user = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'role': role,
            'created_at': datetime.now()
        }
        users.insert_one(user)
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False

def login_user(username, password):
    users = db.users
    user = users.find_one({'username': username})
    
    if user and check_password(password, user['password']):
        st.session_state.user_role = user.get('role', 'buyer')
        return user
    return None

# Product functions
def get_products(seller_id=None):
    query = {'seller_id': seller_id} if seller_id else {}
    products = db.products.find(query)
    return list(products)

def add_product(name, price, description, image_path, seller_id):
    product = {
        'name': name,
        'price': float(price),
        'description': description,
        'image_path': image_path,
        'seller_id': seller_id,
        'created_at': datetime.now()
    }
    db.products.insert_one(product)

def add_to_cart(product):
    st.session_state.cart.append(product)

def remove_from_cart(index):
    st.session_state.cart.pop(index)

# Page functions
def show_home():
    st.markdown("""
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Family Marketing Place</h1>
                <p class="hero-subtitle">Everything for Your Family's Happiness</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    products = get_products()
    cols = st.columns(3)
    
    for idx, product in enumerate(products):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                    <div class="product-card">
                        <img src="{product.get('image_path', 'placeholder.jpg')}" style="width:100%">
                        <h3>{product['name']}</h3>
                        <p class="price">${product['price']:.2f}</p>
                        <p>{product['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Add to Cart", key=f"add_{idx}"):
                    add_to_cart(product)
                    st.success("Added to cart!")

def show_login():
    st.markdown('<div class="header"><h1>Login</h1></div>', unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def show_register():
    st.markdown('<div class="header"><h1>Register</h1></div>', unsafe_allow_html=True)
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Register as", ["buyer", "seller"])
        
        if st.form_submit_button("Register"):
            if password != confirm_password:
                st.error("Passwords do not match!")
                return
            
            if register_user(username, password, email, role):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username or email already exists!")

def show_seller_dashboard():
    st.markdown('<div class="header"><h1>Seller Dashboard</h1></div>', unsafe_allow_html=True)
    
    with st.form("add_product_form"):
        st.subheader("Add New Product")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        description = st.text_area("Description")
        image_path = st.text_input("Image URL")
        
        if st.form_submit_button("Add Product"):
            add_product(name, price, description, image_path, str(st.session_state.user['_id']))
            st.success("Product added successfully!")
    
    st.subheader("Your Products")
    seller_products = get_products(str(st.session_state.user['_id']))
    for product in seller_products:
        with st.container():
            st.markdown(f"""
                <div class="product-card">
                    <h3>{product['name']}</h3>
                    <p class="price">${product['price']:.2f}</p>
                    <p>{product['description']}</p>
                </div>
            """, unsafe_allow_html=True)

def show_admin_dashboard():
    st.markdown('<div class="header"><h1>Admin Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Add tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Live Updates", "Users", "Products", "Orders"])
    
    with tab1:
        st.subheader("📊 Database Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            user_count = db.users.count_documents({})
            st.metric(label="Total Users", value=user_count)
            
        with col2:
            product_count = db.products.count_documents({})
            st.metric(label="Total Products", value=product_count)
            
        with col3:
            order_count = db.orders.count_documents({})
            st.metric(label="Total Orders", value=order_count)
        
        st.subheader("🔄 Recent Activities")
        
        # Recent Users
        st.markdown("##### Latest Users")
        recent_users = list(db.users.find().sort('created_at', -1).limit(5))
        for user in recent_users:
            with st.container():
                st.markdown(f"""
                    <div class="admin-section" style="padding: 1rem; margin-bottom: 0.5rem;">
                        <p><strong>Username:</strong> {user['username']}</p>
                        <p><strong>Email:</strong> {user['email']}</p>
                        <p><strong>Role:</strong> {user.get('role', 'buyer')}</p>
                        <p><strong>Joined:</strong> {user['created_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Recent Orders
        st.markdown("##### Latest Orders")
        recent_orders = list(db.orders.find().sort('created_at', -1).limit(5))
        for order in recent_orders:
            user = db.users.find_one({'_id': order['user_id']})
            with st.container():
                st.markdown(f"""
                    <div class="admin-section" style="padding: 1rem; margin-bottom: 0.5rem;">
                        <p><strong>Order ID:</strong> {str(order['_id'])}</p>
                        <p><strong>Customer:</strong> {user['username'] if user else 'Unknown'}</p>
                        <p><strong>Amount:</strong> ${order['total_amount']:.2f}</p>
                        <p><strong>Items:</strong> {len(order['items'])}</p>
                        <p><strong>Date:</strong> {order['created_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("👥 User Management")
        
        # User filters
        role_filter = st.selectbox("Filter by Role", ["All", "buyer", "seller", "admin"])
        search_term = st.text_input("Search Users", "")
        
        # Build query
        query = {}
        if role_filter != "All":
            query['role'] = role_filter
        if search_term:
            query['$or'] = [
                {'username': {'$regex': search_term, '$options': 'i'}},
                {'email': {'$regex': search_term, '$options': 'i'}}
            ]
        
        users = list(db.users.find(query))
        st.write(f"Found {len(users)} users")
        
        for user in users:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                        <div class="admin-section">
                            <p><strong>Username:</strong> {user['username']}</p>
                            <p><strong>Email:</strong> {user['email']}</p>
                            <p><strong>Role:</strong> {user.get('role', 'buyer')}</p>
                            <p><strong>Created:</strong> {user['created_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                        </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("🛍️ Product Management")
        
        # Product filters
        price_range = st.slider("Price Range", 0, 2000, (0, 2000))
        search_product = st.text_input("Search Products", "")
        
        # Build query
        query = {'price': {'$gte': price_range[0], '$lte': price_range[1]}}
        if search_product:
            query['$or'] = [
                {'name': {'$regex': search_product, '$options': 'i'}},
                {'description': {'$regex': search_product, '$options': 'i'}}
            ]
        
        products = list(db.products.find(query))
        st.write(f"Found {len(products)} products")
        
        cols = st.columns(2)
        for idx, product in enumerate(products):
            with cols[idx % 2]:
                seller = db.users.find_one({'_id': ObjectId(product['seller_id'])}) if product.get('seller_id') != 'sample' else None
                st.markdown(f"""
                    <div class="admin-section">
                        <img src="{product['image_path']}" style="width:100%; border-radius:5px; margin-bottom:10px;">
                        <h3>{product['name']}</h3>
                        <p><strong>Price:</strong> ${product['price']:.2f}</p>
                        <p><strong>Seller:</strong> {seller['username'] if seller else 'Sample Product'}</p>
                        <p>{product['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("📦 Order Management")
        
        # Order filters
        date_range = st.date_input("Date Range", value=[])
        min_amount = st.number_input("Minimum Order Amount", value=0.0)
        
        # Build query
        query = {'total_amount': {'$gte': min_amount}}
        if len(date_range) == 2:
            start_date = datetime.combine(date_range[0], datetime.min.time())
            end_date = datetime.combine(date_range[1], datetime.max.time())
            query['created_at'] = {'$gte': start_date, '$lte': end_date}
        
        orders = list(db.orders.find(query).sort('created_at', -1))
        st.write(f"Found {len(orders)} orders")
        
        total_revenue = sum(order['total_amount'] for order in orders)
        st.metric("Total Revenue", f"${total_revenue:.2f}")
        
        for order in orders:
            user = db.users.find_one({'_id': order['user_id']})
            with st.container():
                st.markdown(f"""
                    <div class="admin-section">
                        <h3>Order #{str(order['_id'])[-6:]}</h3>
                        <p><strong>Customer:</strong> {user['username'] if user else 'Unknown'}</p>
                        <p><strong>Amount:</strong> ${order['total_amount']:.2f}</p>
                        <p><strong>Date:</strong> {order['created_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p><strong>Shipping Address:</strong> {order.get('shipping_address', 'N/A')}</p>
                        <details>
                            <summary>Order Items ({len(order['items'])})</summary>
                            <ul>
                                {''.join(f"<li>{item['name']} - ${item['price']:.2f}</li>" for item in order['items'])}
                            </ul>
                        </details>
                    </div>
                """, unsafe_allow_html=True)

def show_cart():
    st.markdown('<div class="header"><h1>Shopping Cart</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("Your cart is empty!")
        return
    
    total = 0
    for idx, item in enumerate(st.session_state.cart):
        st.markdown(f"""
            <div class="cart-item">
                <div>
                    <h3>{item['name']}</h3>
                    <p>${item['price']:.2f}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Remove", key=f"remove_{idx}"):
            remove_from_cart(idx)
            st.rerun()
        total += item['price']
    
    st.markdown(f"""
        <div class="cart-item">
            <h2>Total: ${total:.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Proceed to Checkout"):
        if not st.session_state.user:
            st.warning("Please login first!")
            return
        st.session_state.checkout = True
        st.rerun()

def show_checkout():
    st.markdown('<div class="header"><h1>Checkout</h1></div>', unsafe_allow_html=True)
    
    total = sum(item['price'] for item in st.session_state.cart)
    
    st.markdown(f"""
        <div class="cart-item">
            <h2>Total Amount: ${total:.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("checkout_form"):
        st.subheader("Shipping Information")
        address = st.text_area("Shipping Address")
        
        st.subheader("Payment Information")
        card_number = st.text_input("Card Number")
        col1, col2 = st.columns(2)
        with col1:
            expiry = st.text_input("Expiry (MM/YY)")
        with col2:
            cvv = st.text_input("CVV", type="password")
        
        if st.form_submit_button("Place Order"):
            try:
                order = {
                    'user_id': st.session_state.user['_id'],
                    'items': st.session_state.cart,
                    'total_amount': total,
                    'shipping_address': address,
                    'status': 'completed',
                    'created_at': datetime.now()
                }
                db.orders.insert_one(order)
                
                st.session_state.cart = []
                st.success("Order placed successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error processing payment: {str(e)}")

def main():
    load_css()
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    if st.session_state.user:
        st.sidebar.write(f"Welcome, {st.session_state.user['username']}!")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.session_state.user_role = None
            st.rerun()
    
    # Different navigation options based on user role
    if st.session_state.user_role == 'admin':
        page = st.sidebar.radio("Go to", ["Home", "Admin Dashboard", "Cart"])
    elif st.session_state.user_role == 'seller':
        page = st.sidebar.radio("Go to", ["Home", "Seller Dashboard", "Cart"])
    else:
        page = st.sidebar.radio("Go to", ["Home", "Login", "Register", "Cart"])
    
    # Display cart count in sidebar
    st.sidebar.write(f"Cart Items: {len(st.session_state.cart)}")
    
    if page == "Home":
        show_home()
    elif page == "Login":
        show_login()
    elif page == "Register":
        show_register()
    elif page == "Cart":
        show_cart()
    elif page == "Seller Dashboard" and st.session_state.user_role == 'seller':
        show_seller_dashboard()
    elif page == "Admin Dashboard" and st.session_state.user_role == 'admin':
        show_admin_dashboard()
    
    if hasattr(st.session_state, 'checkout') and st.session_state.checkout:
        show_checkout()

if __name__ == "__main__":
    main()
