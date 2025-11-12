# Shop (Django E-Commerce)

A modular Django-based e-commerce sample dockerized project with ZarinPal gateway, products caching using Redis, products listing, filtering and pagination features.

## ✨ Features
- ZarinPal Gate
- Dockerized
- Caching using Redis
- Product listing with pagination
- Filter products by:
  - Color
  - Size
  - Price range (min / max)
- Filters persist while navigating between pages
- Authentication system (login, signup)
- Organized multi-app structure (account, product, cart, home)
- Bootstrap-based UI
- SQLite used for easy local development

## Tech Stack
- Python 3
- Django
- Docker & DockerCompose
- Redis
- SQLite 
- JS/ HTML / CSS / Bootstrap

## 🏗️ Project Structure
```
multi_shop3/
├── apps/
│ ├── account/
│ ├── cart/
│ ├── home/
│ └── product/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```
## 🚀 Installation

### 1. Clone the repository
```
git clone https://github.com/mohamadArdebili/django-shop.git
cd multi_shop3
```
### 2. Create and activate virtual environment
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```
### 5. Create admin user (optional)
```
python manage.py createsuperuser
```
### 6. Run the server
```
python manage.py runserver
```
### Visit:
```
http://127.0.0.1:8000/
```
### 🔍 Filtering Example
```
/products/?color=Red&size=L&min_price=50&max_price=200&page=2
```
## 📌 Future Enhancements
- REST API with Django REST Framework
  
- Shopping cart and checkout system

- User profile pages

- Product search bar (with autocomplete)

## 🤝 Contributions

Feel free to fork, build features, or open issues for improvements.  
