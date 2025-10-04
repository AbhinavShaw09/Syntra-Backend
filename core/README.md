# Shopless Core API

This repository contains the core backend API for **Shopless**, a modern, headless e-commerce platform built with Django and Django REST Framework. It provides all the necessary functionalities for managing products, users, orders, and payments.

## Key Features

- **Authentication:** Secure user authentication using JSON Web Tokens (JWT).
- **Store Management:** Functionality for product and category management.
- **Buyer-centric Flows:** Cart management, order placement, and address handling.
- **Payment Integration:** A modular payment system with an initial implementation for Razorpay.
- **Comprehensive Test Suite:** Unit and integration tests to ensure code quality and reliability.

## Architecture

The project follows a robust and scalable architecture, leveraging the power of Django while incorporating best practices for API development.

- **Framework:** Built on [Django](https://www.djangoproject.com/) and [Django REST Framework (DRF)](https://www.django-rest-framework.org/) for rapid and secure API development.
- **Service Layer:** Business logic is encapsulated within a **Service Layer** (`api/services/`). This separates the core logic from the view/controller layer, promoting cleaner code, easier testing, and better maintainability. Views in `api/views/` delegate all business operations to these services.
- **Modular Design:** The application is organized into a single Django app, `api`, which is further divided into logical modules like `accounts`, `store`, `orders`, and `payments`.
- **Pluggable Payment System:** The payment processing logic is designed to be extensible. A base payment service (`api/services/payments/base.py`) defines the interface, allowing for multiple payment gateway implementations (like `razorpay.py`) to be added with minimal effort.
- **Configuration:** Project settings are managed via environment variables (`.env` file), following the 12-factor app methodology.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.10+
- Pip (Python package installer)
- A virtual environment tool (like `venv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd shopless/core
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory by copying the example below. Be sure to fill in your actual credentials.

    ```env
    # .env
    SECRET_KEY='your-django-secret-key'
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost

    # Database (example for local SQLite)
    DB_ENGINE=django.db.backends.sqlite3
    DB_NAME=db.sqlite3

    # Razorpay Credentials
    RAZORPAY_KEY_ID=your_key_id
    RAZORPAY_KEY_SECRET=your_key_secret
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## Running Tests

To run the test suite, execute the following command:

```bash
python manage.py test
```

## Linting

This project uses `ruff` for linting. A shell script is provided for convenience.

```bash
./lint.sh
```

## Future Plans & Roadmap

This project provides a solid foundation for a full-fledged e-commerce platform. Future enhancements could include:

-   **Frontend Application:** Develop a decoupled frontend using a modern JavaScript framework like React or Vue.js.
-   **Additional Payment Gateways:** Integrate other payment providers like Stripe or PayPal into the modular payment system.
-   **Real-time Functionality:** Add real-time order updates and notifications using Django Channels and WebSockets.
-   **Advanced Product Search:** Implement a robust search feature using a dedicated search engine like Elasticsearch.
-   **Admin Dashboard:** Enhance the Django Admin or build a custom dashboard for better store management.
-   **CI/CD:** Set up a Continuous Integration and Continuous Deployment pipeline to automate testing and deployments.
-   **Containerization:** Dockerize the application for easier development and deployment.
