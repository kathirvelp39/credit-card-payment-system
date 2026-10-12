# Credit Card Payment System

## Project Overview

Credit Card Payment System is a web application developed using Django, FastAPI, and MySQL. It supports user authentication, secure card management, simulated payment processing, transaction history, and administrative monitoring.

## Technologies Used

- Python
- Django and Django REST Framework
- FastAPI
- MySQL
- HTML, CSS, JavaScript
- JWT Authentication
- Pytest and Django Testing Framework
- Postman

## Features

### 1. User Authentication
- User registration and login
- JWT authentication and token refresh
- Logout and protected endpoints
- Password hashing

### 2. Card Management
- Add credit and debit cards
- View and delete saved cards
- Store masked card numbers and last four digits
- Do not store full card numbers or CVV

### 3. Payment Processing
- Simulated payment processing through FastAPI
- Track PENDING, SUCCESS, and FAILED statuses
- Validate card ownership and payment amounts

### 4. Transaction Management
- View transaction history
- Filter by status, amount, and date
- Export transactions to CSV

### 5. Admin Dashboard
- Manage users and cards
- View transactions
- View daily payment summaries
- Review administrative logs

## Prerequisites

- Python 3.12 or another compatible Python version
- MySQL Server
- Git

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kathirvelp39/credit-card-payment-system.git
cd credit-card-payment-system
```

### 2. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference.

Set your own values for:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Do not commit `.env` or real secrets to GitHub.

### 4. Configure MySQL

Create the database configured in your `.env` file. Make sure the MySQL server is running and the database credentials are correct.

### 5. Apply Migrations

```powershell
python manage.py migrate
```

### 6. Create an Admin User

```powershell
python manage.py createsuperuser
```

### 7. Start the Django Server

```powershell
python manage.py runserver
```

Django: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

### 8. Start the FastAPI Server

Open a second terminal, activate the virtual environment, and run:

```powershell
uvicorn payment_api:app --reload --port 8001
```

FastAPI Swagger documentation: http://127.0.0.1:8001/docs

## Testing

Run Django tests:

```powershell
python manage.py test accounts cards transactions
```

Run FastAPI tests:

```powershell
python -m pytest test_fastapi_payment.py -v
```

Check the Django project:

```powershell
python manage.py check
```

### Test Results

- Django tests: 12 passed
- FastAPI tests: 7 passed
- Django code coverage: 69%
- Django system check: no issues identified

Coverage is measured for the Django modules by the reported coverage command; FastAPI tests were run separately.

## Postman API Collection

Import `postman_collection.json` into Postman to test authentication, card management, payment processing, and transaction filtering.

Use test data only. Never use real card details.

## Security Notes

- Keep secrets in `.env`.
- Do not commit `.env`, database dumps, or real credentials.
- Do not store full card numbers or CVV.
- This project simulates payments; it is not a real payment gateway.

## Screenshots

See the `screenshort/` folder for project screenshots.

## Repository

GitHub: https://github.com/kathirvelp39/credit-card-payment-system

## Author

Kathirvel P
