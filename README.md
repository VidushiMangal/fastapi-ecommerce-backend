# FastAPI E-commerce Backend

This is a backend-only e-commerce project built using **FastAPI** and **PostgreSQL**.  
The project focuses on **clean backend flow, data integrity, and real-world order lifecycle**, without any frontend.

The goal of this project is to understand and implement how a real e-commerce backend works internally.
---
## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication
- Postman (for testing)
---
## Project Structure (High Level)
app/
├── auth/ # user registration, login, roles
├── catalog/ # categories and products
├── orders/ # orders, order items, lifecycle
├── payments/ # mocked payment flow
├── core/ # database, security, dependencies
└── main.py

## Core Modules & Flow

### 1. Auth Module
Handles:
- User registration
- User login
- JWT token generation
- Role-based access (admin / customer)

Passwords are **hashed before storing** and never saved in plain text.  
JWT tokens are used to secure protected APIs.

### 2. Catalog Module
Handles:
- Category creation (admin only)
- Product creation (admin only)
- Public product listing

Each product:
- Belongs to a category
- Has price and stock
- Can be browsed publicly without authentication

### 3. Orders Module
Handles:
- Order creation (authenticated users)
- Order items (multiple products per order)
- Inventory validation
- Order lifecycle management

During order creation:
- Product stock is validated
- Product price is copied (price snapshot)
- Total amount is calculated
- Stock is reduced

Order status flow:
        CREATED → PAID → SHIPPED → COMPLETED
                ↘
                FAILED

### 4. Payments Module (Mocked)
Handles:
- Simulated payment success or failure

Payments:
- Can be done only when order status is `CREATED`
- Update order status to `PAID` or `FAILED`
- Do not interact with real payment gateways

This keeps the focus on backend logic and order flow.

### 5. Analytics (Admin Only)
Provides read-only system insights:
- Total orders count
- Total revenue (PAID + COMPLETED orders)
- Orders grouped by status

Analytics use SQL aggregation and do not modify data.

## Real-Life Order Flow Example

1. Admin creates categories and products  
2. User registers and logs in  
3. User browses products  
4. User places an order  
   - Stock is validated  
   - Price snapshot is taken  
5. User makes payment  
   - Order becomes PAID or FAILED  
6. Admin ships and completes the order  
7. Analytics reflect the transaction  

## Why Price Snapshot Is Used

Product prices can change over time.

At order creation:
- The product price is copied into `order_items`
- Old orders remain unchanged even if product prices change later

This ensures historical accuracy and correct revenue reporting.

## Authentication & Access Rules

- Public:
  - View product listings
- Customer:
  - Place orders
  - Make payments
- Admin:
  - Create categories
  - Create products
  - Update order status
  - View analytics

## How to Run the Project
```bash
# create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run server (from project root)
uvicorn app.main:app --reload

Notes

This project intentionally excludes frontend development
Payments are mocked to keep the focus on backend design
Built to understand real-world backend flow through implementation