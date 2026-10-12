\# Credit Card Payment System



\## Project Overview



Credit Card Payment System is a web application developed using Django, FastAPI, and MySQL. It supports user authentication, card management, payment processing, transaction history, and administrative monitoring.



\## Technologies Used



\- Python

\- Django

\- FastAPI

\- MySQL

\- HTML

\- CSS

\- JavaScript

\- JWT Authentication

\- Pytest

\- Django Testing Framework



\## Features



\### 1. User Authentication

\- User registration and login

\- JWT authentication

\- Token refresh and logout

\- Protected endpoints



\### 2. Card Management

\- Add credit and debit cards

\- View saved cards

\- Delete cards

\- Store masked card numbers and last four digits

\- Do not store CVV or full card numbers



\### 3. Payment Processing

\- Process simulated payments

\- Track payment status

\- Support PENDING, SUCCESS, and FAILED statuses

\- Validate card ownership



\### 4. Transaction Management

\- View transaction history

\- Filter transactions by status, amount, and date

\- Export transactions to CSV



\### 5. Admin Dashboard

\- Manage users and cards

\- View transactions

\- View daily payment summaries

\- Review administrative logs



\## Installation and Setup



\### Prerequisites

\- Python

\- MySQL Server

\- Git



\### 1. Clone the Repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd credit\_card\_payment\_system

