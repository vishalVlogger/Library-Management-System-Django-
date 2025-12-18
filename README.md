# 📚 Library Management System (Django)

A **role-based Library Management System** built using **Django** that allows staff to manage books and users to issue/return books safely.  
The project focuses on **inventory safety, clean UI, role-based access, and proper transaction tracking**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![HTML](https://img.shields.io/badge/HTML-4.0+-orange.svg)

---

## 🚀 Features

### 👤 User Roles
- **Staff (Admin)**
  - Add, edit, and delete books
  - View all books with stock details
  - View all users
  - Track all issue & return transactions with date and time
- **User (Member)**
  - View available books
  - Issue books (only if stock is available)
  - View issued books
  - Return books
  - Track issue & return history

---

## 📚 Book Management
- Book details include:
  - Title, Subtitle
  - Author(s)
  - ISBN
  - Publisher
  - Category
  - Description
  - Price
  - Cover Image
  - Total Quantity
  - Available Quantity
- Inventory is **automatically updated** on issue/return
- Prevents:
  - Issuing when stock = 0
  - Returning beyond total stock

---

## 🔄 Transaction Management
- Tracks:
  - Issue Date & Time
  - Return Date & Time
  - Quantity
  - Status (Issued / Returned)
- Fully timezone-aware (`localtime`)
- Clean transaction history for:
  - Individual users
  - Staff dashboard

---

## 🧠 Business Logic Highlights
- Role-based access control (Staff vs User)
- Safe inventory handling
- Django ORM best practices
- Clean separation of views, templates, forms, and models
- Server-side validation + user-friendly messages

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Bootstrap 5
- **Database:** SQLite (can be switched to PostgreSQL/MySQL)
- **Authentication:** Django Auth
- **Styling:** Bootstrap 5
- **Media Handling:** Django Media Files

---

## 📂 Project Structure
```bash
library_management/
│
├── inventory/
│ ├── migrations/
│ ├── templates/
│ │ └── inventory/
│ │ ├── base.html
│ │ ├── book_list.html
│ │ ├── book_detail.html
│ │ ├── book_form.html
│ │ ├── book_confirm_delete.html
│ │ ├── my_books.html
│ │ └── staff_dashboard.html
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── urls.py
│ └── auth_views.py
│
├── media/
├── static/
├── db.sqlite3
├── manage.py

```
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```
### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```
### 3️⃣ Install dependencies
```bash
pip install django
```
### 4️⃣ Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5️⃣ Create superuser
```bash
python manage.py createsuperuser
```
### 6️⃣ Run the server
```bash
python manage.py runserver
```
### Visit:
```bash
👉 http://127.0.0.1:8000/
```
---

### 🔐 Authentication Flow
          
- Signup with role:
  - STAFF → Admin features enabled
  - USER → Member features enabled
- The staff dashboard is accessible only to staff users
- Users cannot access staff routes
  
---

### 📸 Screens (Suggested)

- You can add screenshots later:
- Book List
- Staff Dashboard
- Book Detail Page
- My Books Page

---

### 🎯 Future Enhancements

- Due date & fine calculation
- Book a reservation system
- Pagination & search filters
- Email notifications
- REST API with Django REST Framework

---

### 👨‍💻 Author

Vishal Patil
- Salesforce Developer → Data Analyst / Python Developer Aspirant
- Built as a hands-on Django project to strengthen backend + full-stack skills.
