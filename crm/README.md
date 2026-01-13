📅 Task Scheduling & Automation in Django (GraphQL CRM)

This project demonstrates how to automate background and scheduled tasks in a Django + GraphQL CRM application using system cron jobs and GraphQL queries. It focuses on real-world backend automation such as data cleanup and sending order reminders without blocking the main application.

🚀 Project Overview

The CRM application supports automated maintenance and notification workflows using cron jobs. Two key scheduled tasks are implemented:

Customer Cleanup Task
Deletes inactive customers who have no orders for over one year.

Order Reminder Task
Queries the GraphQL API to find recent pending orders and logs reminder information.

These tasks are designed to run automatically at predefined times using Unix cron.

🎯 Learning Objectives

By completing this project, you will be able to:

Explain what cron jobs are and how they work

Write and schedule cron jobs using crontab

Automate Django tasks using shell and Python scripts

Query a Django GraphQL API programmatically

Log and debug automated background processes

Apply best practices for scheduled task management

🛠️ Technologies Used

Python 3

Django 4.2

Graphene-Django (GraphQL)

gql (GraphQL client)

Unix Cron

SQLite (development database)

📁 Relevant Project Structure
crm/
└── cron_jobs/
    ├── clean_inactive_customers.sh
    ├── customer_cleanup_crontab.txt
    ├── send_order_reminders.py
    └── order_reminders_crontab.txt

🧹 Task 0: Customer Cleanup Cron Job
Description

A shell script that runs a Django ORM command to delete customers who:

Have no related orders

Were created more than one year ago

Script

File: crm/cron_jobs/clean_inactive_customers.sh

Features:

Uses manage.py shell

Logs number of deleted customers

Writes logs to /tmp/customer_cleanup_log.txt

Includes timestamped output

Cron Schedule

File: crm/cron_jobs/customer_cleanup_crontab.txt

Runs every Sunday at 2:00 AM:

0 2 * * 0 /absolute/path/to/crm/cron_jobs/clean_inactive_customers.sh

🔔 Task 1: Order Reminder Automation (GraphQL)
Description

A Python script that queries the GraphQL API to find orders created within the last 7 days and logs reminder details.

Script

File: crm/cron_jobs/send_order_reminders.py

Features:

Uses the gql library

Queries http://localhost:8000/graphql

Fetches order ID and customer email

Logs results to /tmp/order_reminders_log.txt

Prints confirmation message on completion

Cron Schedule

File: crm/cron_jobs/order_reminders_crontab.txt

Runs daily at 8:00 AM:

0 8 * * * /usr/bin/python3 /absolute/path/to/crm/cron_jobs/send_order_reminders.py

🧪 Manual Testing
Run Django Server
python3 manage.py runserver

Test Cleanup Script
crm/cron_jobs/clean_inactive_customers.sh
cat /tmp/customer_cleanup_log.txt

Test Order Reminder Script
crm/cron_jobs/send_order_reminders.py
cat /tmp/order_reminders_log.txt

📦 Required Dependencies

Install required packages:

pip install graphene-django django-filter gql requests

✅ Best Practices Applied

✔ Absolute paths in cron jobs

✔ Output logging for debugging

✔ Idempotent task design

✔ Separation of concerns (cron vs business logic)

✔ GraphQL used for read-only automation

🌍 Real-World Use Cases

Removing stale or inactive user accounts

Sending order or payment reminders

Generating scheduled reports

Cleaning up expired tokens or sessions

Running heavy background jobs during off-peak hours

📝 Assessment Notes (ALX)

All required files are present

Cron schedules are correctly defined

Scripts are executable

Logs are written to /tmp

Project is ready for manual and peer review

👨‍💻 Author

Pius Ndubi
Backend / Full-Stack Developer
Django · GraphQL · Automation · Cron · Celery

# CRM Weekly Report Automation

This project uses Celery and Celery Beat to generate a weekly CRM report using GraphQL data.

## Setup Instructions

### 1. Install Redis
```bash
sudo apt update
sudo apt install redis-server
