# BUFET Website

## Overview
Bufet System is a web application built using Django, providing a platform for users to browse a menu, add dishes to their cart, and place orders from various restaurants. The system supports user authentication, allowing users to track their orders and manage their cart.

## Installation and Deployment
1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/bufet-system.git
    cd bufet-system
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser account (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the application in your web browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

### Usage

- Visit the main page to view the menu and explore restaurants.
- Log in or create an account to add dishes to your cart.
- Access your cart to review selected items and quantities.
- Proceed to checkout, select a restaurant, and place your order.
