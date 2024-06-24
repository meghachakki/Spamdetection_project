### Spamdetection_project
## Overview
This project is a web-based chat application developed using Django framework. It allows registered users to send messages to each other, mark messages as read, detect spam messages, and manage contacts.

## Features
User Authentication: Users can sign up, log in, and log out securely.
Profile: Each user has a profile page displaying their contacts, chat history, and options to add/remove contacts.
Messaging System: Users can send messages to each other. Messages can be marked as read.
Spam Detection: Implemented a basic spam detection mechanism to flag potential spam messages.
Email Spam Alerts: Automated email notifications are sent when multiple spam messages are detected:
Spam Alert: Sent to the recipient when multiple spam messages are received from a sender.
Spam Warning: Sent to the sender when they send multiple spam messages.
Contact Management: Users can add and remove contacts from their profile.
Security: CSRF protection, authentication, and authorization are implemented to secure the application.
## Technologies Used
Django: Python web framework used for backend development.
HTML/CSS: Frontend design and structure.
JavaScript (jQuery): Used for asynchronous operations like marking messages as read.
SQLite: Database for storing user data and chat messages.
## Setup Instructions
Clone the Repository: git clone <repository-url>
Navigate to the Project Directory: cd chat-application
Create a Virtual Environment: python -m venv venv
Activate Virtual Environment:
On Windows: venv\Scripts\activate
On macOS/Linux: source venv/bin/activate
Install Dependencies: pip install -r requirements.txt
Apply Migrations: python manage.py migrate
Load Initial Data (Optional): python manage.py loaddata initial_data
Run the Development Server: python manage.py runserver
Access the Application: Open your web browser and go to http://localhost:8000
## Folder Structure
/chat/: Django application directory.
/static/: Static files (CSS, JS, images).
/templates/: HTML templates.
/venv/: Virtual environment folder (not included in repository).
## Additional Notes
Customize the application as per your requirements.
For production deployment, configure a suitable database backend like PostgreSQL.
Ensure proper error handling and logging in production environments.
Ensure that email backend settings are configured in Django settings (settings.py) for email spam alerts to function properly.
