# 💸 BUDGETARIAN

Welcome to the BUDGETARIAN — your friendly companion for managing money like a pro. Whether you're saving up for a dream vacation or just want to keep your daily spending in check, this app has got you covered.

---

## Key Features

### 🔐 Secure User Accounts

* Create an account to get started
* Log in, log out, and manage your sessions with ease
* Your financial data stays yours — private and secure

### 💰 Track Your Finances

* Add income and expense entries quickly
* Include details like title, amount, date, type, and notes
* Edit or delete your records anytime — flexibility at your fingertips

### 🗂 Organize with Categories

* Assign categories to your expenses (e.g., Food, Bills, Travel)
* Keep your finances tidy and easy to analyze

### 📊 Visual Summaries & Dashboard

* Monitor your monthly financial activity at a glance
* Pie chart for spending breakdown by category
* Bar graph showing income vs. expenses over time
* Dashboard with totals, balance, and handy shortcuts

### 🎯 Budgeting Tools

* Set monthly budgets per category or overall
* Receive alerts when you go over budget

### 📤 Data Export

* Export your financial data as CSV
* Useful for reports, backups, or switching tools

---

## 🛠 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/caloyyyy0203/personal-budget-tracker.git
cd personal-budget-tracker
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv

# On Macos/Linux:

source venv/bin/activate  

# On Windows: 

venv\Scripts\activate
```

### Step 3: Install the Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

### Step 5: (Optional) Create Admin User

```bash
python manage.py createsuperuser
```

### Step 6: Start the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to explore the app in action.

---

## 👩‍💼 Getting Started Guide

### Explore Your Dashboard

* See your total income, expenses, and remaining balance
* View charts that bring your spending habits to life

### Add a New Entry

* Use the **Add Entry** form
* Select income or expense, add details, and submit

### Manage Your History

* Navigate to **View History**
* Edit or delete entries with just a few clicks

---

## 🧩 Tech Stack

* Django (Web framework)
* HTML & CSS (Frontend styling)
* Chart.js (Interactive charts)
* SQLite (Database)


Manage your money, stress less. Happy budgeting! 🎉
