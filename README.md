# Streamlit E-commerce Website

A full-featured e-commerce website built with Streamlit, featuring user authentication, product catalog, shopping cart, and checkout functionality.

## Features

- User Registration and Login
- Product Catalog
- Shopping Cart
- Secure Checkout Process
- Order History
- Responsive Design

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Stripe API key:
```
STRIPE_SECRET_KEY=your_stripe_secret_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Register a new account or login with existing credentials
2. Browse products on the home page
3. Add items to your cart
4. Proceed to checkout when ready
5. Enter shipping and payment information
6. Complete your purchase

## Security

- Passwords are hashed using bcrypt
- Payment processing is handled securely through Stripe
- User sessions are managed securely
- Database uses SQLite with proper security measures

## Development

To add new products to the database, use the SQLite command line or a DB browser to insert records into the products table.
