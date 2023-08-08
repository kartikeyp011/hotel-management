# Taj Hotel Management System

Welcome to the Taj Hotel Management System! This Python code provides a comprehensive command-line interface for efficiently managing various aspects of hotel operations, including customer reservations, room bookings, and user account management. The system employs a MySQL database to securely store customer information, room details, and booking records.

## Prerequisites

Before you begin, ensure you have the following components set up:

- Python 3.x installed on your machine.
- A MySQL database named `hotel_management` created and accessible either locally or on a remote server.
- The necessary Python libraries, such as `mysql-connector`, installed. You can install them using the following command:

```
pip install mysql-connector-python
```

## Getting Started

1. Clone or download this repository to your local machine.
2. Open the `taj_hotel_management.py` script in your preferred Python IDE or text editor.
3. Update the database connection details in the script to match your MySQL configuration. Modify the `host`, `user`, `password`, and `database` parameters according to your setup.

## Usage Instructions

1. Run the script in your terminal or Python environment.
2. Upon execution, the system will warmly greet you with a beautiful Taj Hotel welcome message.
3. Choose between the following options:

   - **Login**: If you have an existing account, provide your email and password to log in.
   - **Sign Up**: If you're new here, create an account by entering your email, name, and a secure password.

4. Once logged in, you'll have access to the following features:

   - View your current bookings.
   - Book a room for your desired stay.
   - Update your account information, including your name and password.
   - Log out from the system.

5. The system will guide you through each step with clear prompts and instructions.

## Security Questions

To ensure the security of your account, the system uses security questions for both sign-up and password recovery processes. Make sure to choose questions and answers that are difficult for others to guess while being memorable to you.

## Subscription Benefits

Subscribed users receive exclusive benefits, including discounts on room prices based on their subscription level: Silver, Gold, Platinum, or Diamond. The system will automatically apply the appropriate discount during room booking for subscribed users.

## Data Management

The system efficiently manages customer data, room information, and booking records within the MySQL database. You can further manage this data using standard MySQL commands or popular database management tools.

## Important Notes

- This code provides a simplified yet functional representation of a hotel management system.
- Feel free to customize and extend the code to match your specific requirements and business logic.
- Remember to sanitize user inputs and implement additional security measures in a production environment.

## Author

The Taj Hotel Management System is developed by Kartikey Narain Prajapati. If you have any questions or need assistance, please reach out to knprajapati08@gmail.com
