
# **SusDevOSMVP**

## **Overview**

**SusDevOSMVP** is a robust, scalable backend built using the Django framework. It provides user authentication, authorization, and password management with production-grade features like OAuth2 token-based authentication, Role-Based Access Control (RBAC), and secure password reset workflows. The project is optimized for PostgreSQL and Python 3.12, making it suitable for high-performance and production-grade applications.

---

## **Features**

- **Authentication**:
  - Token-based authentication using OAuth2.
  - Secure login with encrypted passwords.
- **Password Management**:
  - Password reset via email with time-limited secure tokens.
  - Password change notifications.
- **Authorization**:
  - Role-Based Access Control (RBAC) with Django Guardian.
  - Attribute-Based Access Control (ABAC) for granular permissions.
- **Security**:
  - Enforced HTTPS in production.
  - CSRF protection and session security.
  - Rate limiting for sensitive API endpoints.
- **Email Notifications**:
  - Password reset and account notifications.
  - Configurable SMTP backend.

---

## **Technology Stack**

- **Language**: Python 3.12
- **Framework**: Django
- **Database**: PostgreSQL
- **Authentication**: OAuth2
- **Permissions**: Django Guardian (RBAC)
- **Email**: SMTP (e.g., Gmail, AWS SES)

---

## **Prerequisites**

- Python 3.12
- PostgreSQL 12+
- Virtual Environment Manager (e.g., `venv` or `virtualenv`)

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/SusDevOSMVP.git
cd SusDevOSMVP
```

### **2. Set Up Virtual Environment**
```bash
python3.12 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**
Create a `.env` file in the root directory:
```dotenv
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,localhost

DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

### **5. Set Up PostgreSQL**
Create the PostgreSQL database:
```sql
CREATE DATABASE your_database_name;
CREATE USER your_database_user WITH PASSWORD 'your_database_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_database_user;
```

### **6. Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **7. Create a Superuser**
```bash
python manage.py createsuperuser
```

### **8. Run the Development Server**
```bash
python manage.py runserver
```

The server will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## **API Documentation**

### **Authentication**

#### **Login**
- **Endpoint**: `POST /auth/login`
- **Request**:
  ```json
  {
    "user_email": "user@example.com",
    "password": "SecurePassword123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "user@example.com"
    }
  }
  ```

#### **Password Reset Request**
- **Endpoint**: `POST /auth/password-reset/request`
- **Request**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Password reset email sent."
  }
  ```

#### **Password Reset Confirm**
- **Endpoint**: `POST /auth/password-reset/confirm`
- **Request**:
  ```json
  {
    "uid": "encoded-user-id",
    "token": "reset-token",
    "new_password": "NewSecurePassword123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Password updated successfully."
  }
  ```

---

## **Deployment**

### **Production Settings**
Update `settings.py` for production:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### **Static Files**
Collect static files:
```bash
python manage.py collectstatic
```

### **Deploy with Gunicorn and Nginx**
1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```
2. Run Gunicorn:
   ```bash
   gunicorn SusDevOSMVP.wsgi:application --bind 0.0.0.0:8000
   ```
3. Configure Nginx to proxy requests to Gunicorn.

---

## **Testing**

Run the test suite:
```bash
python manage.py test
```

---

## **Contributing**

Contributions are welcome! Please fork the repository and create a pull request with your changes.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**

- **Author**: Your Name
- **Email**: your-email@example.com
- **GitHub**: [https://github.com/your-username](https://github.com/your-username)

---

## **Project Structure**

```
SusDevOSMVP/
    ├── SusDevOSMVP/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   ├── asgi.py
    ├── auth_app/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── serializers.py
    │   └── tests.py
    ├── manage.py
    ├── .env
    ├── requirements.txt
    ├── README.md
```
