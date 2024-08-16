# SaaS Sample Project

This is a sample SaaS (Software as a Service) project built using Django. The project demonstrates a basic SaaS application setup with payment processing integrated via Stripe, and it's hosted on [Railway](https://railway.app) with a PostgreSQL database hosted on [Neon](https://neon.tech).

## Features

- **User Authentication**: Secure user registration, login, and password management.
- **Subscription Plans**: Multiple pricing plans (Basic, Pro, Advanced Pro) with tiered features.
- **Stripe Integration**: Payment processing via Stripe for handling subscriptions and billing.
- **Admin Dashboard**: Manage users, subscriptions, and payments from a central dashboard.
- **Responsive UI**: Built with responsive design principles, including light and dark mode options.

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Payment Gateway**: Stripe
- **Database**: PostgreSQL (hosted on Neon)
- **Hosting**: Railway

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/judeVector/saas-sample-project.git
   cd saas-application
   ```

2. **Create and activate a virtual environment:**

   ```bash
       python3 -m venv env
       source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
        pip install -r requirements.txt
   ```

### Set up the database:

- Configure your PostgreSQL database settings in `settings.py`.
- Run migrations:

  ```bash
  python manage.py migrate
  ```

### Configure Stripe:

- Add your Stripe API keys in settings.py.
- Set up Stripe Webhooks if needed.
- Run the development server:

```bash
python manage.py runserver
```

### Access the application:

Visit http://127.0.0.1:8000/ in your browser to see the application in action.
