# Shopless

A modern, headless e-commerce platform built with Django and Django REST Framework.

## Overview

Shopless is a comprehensive backend API solution for e-commerce applications, providing all the essential functionalities needed to build a scalable online store. The platform follows a headless architecture, allowing for flexible frontend implementations while maintaining a robust and secure backend.

## Key Features

- **Secure Authentication**: JWT-based user authentication system
- **Store Management**: Complete product and category management
- **Order Processing**: Full order lifecycle management from cart to delivery
- **Payment Integration**: Modular payment system with Razorpay support
- **User Management**: Buyer and seller account management
- **Address Handling**: Comprehensive address management for orders
- **Comprehensive Testing**: Extensive unit and integration test coverage

## Architecture

The project is built with:
- **Django & Django REST Framework**: For rapid and secure API development
- **Service Layer Architecture**: Clean separation of business logic
- **Modular Design**: Organized into logical modules (accounts, store, orders, payments)
- **Pluggable Payment System**: Extensible payment gateway integration
- **Environment-based Configuration**: Following 12-factor app methodology

## Project Structure

```
shopless/
├── core/                 # Main Django application
│   ├── api/             # API modules
│   │   ├── models/      # Database models
│   │   ├── views/       # API views
│   │   ├── serializers/ # Data serializers
│   │   ├── services/    # Business logic layer
│   │   └── tests/       # Test suites
│   ├── manage.py        # Django management script
│   └── requirements.txt # Python dependencies
└── README.md           # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbhinavShaw09/Syntra-Backend.git
   cd shopless
   ```

2. **Start the application**
   ```bash
   ./run start
   ```

The API will be available at `http://localhost:8000`

### Docker Commands

```bash
./run start    # Start the application
./run stop     # Stop the application
./run restart  # Restart the application
./run logs     # View application logs
./run build    # Build the application
./run clean    # Clean up containers and volumes
```

### Manual Setup (Alternative)

If you prefer to run without Docker:

1. **Prerequisites**
   - Python 3.10+
   - PostgreSQL
   - pip and virtual environment tool

2. **Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   cd core
   pip install -r requirements.txt
   cp .env.example .env  # Configure your database settings
   python manage.py migrate
   python manage.py runserver
   ```

## API Documentation

The API provides endpoints for:
- User authentication and account management
- Product and category management
- Shopping cart operations
- Order processing and tracking
- Payment processing
- Address management

## Testing

Run the comprehensive test suite:
```bash
cd core
python manage.py test
```

## Development

### Code Quality
```bash
./lint.sh  # Run linting with ruff
```

### Database
The project supports multiple database backends. Configure your preferred database in the `.env` file.

## Deployment

### Docker Deployment

The application includes Docker configuration for easy deployment:

- **docker-compose.yml**: Orchestrates the web application and PostgreSQL database
- **Dockerfile**: Containerizes the Django application
- **./run script**: Provides convenient commands for container management

For production deployment, update the environment variables in docker-compose.yml and ensure proper security configurations.

### Manual Deployment

The application is designed to be easily deployable to various platforms. Refer to the core directory's README for detailed deployment instructions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please open an issue on GitHub.
