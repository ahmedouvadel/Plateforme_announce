📢 Django Annonce Management System

A Django-based web application for managing advertisements and categories through the admin interface. This project allows you to create, update, and organize ads with various statuses (Pending, Approved, Rejected) and categories (Electronics, Real Estate, etc.).

🛠️ Features:
Category Management: Add and manage categories for advertisements.
Advertisement Management: Create, update, and delete ads with details like title, description, price, image, and category.
Admin Customization: Enhanced Django admin interface with custom actions (Approve/Reject), search, and filters.
Status Tracking: Manage ad statuses (Pending, Approved, Rejected) using Django TextChoices.
📌 How to Run:
Clone the repository:
bash
Copier
Modifier
git clone https://github.com/ahmedouvadel/Plateforme_announce
cd your-repo
Set up a virtual environment and install dependencies:
bash
Copier
Modifier
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Apply migrations and create a superuser:
bash
Copier
Modifier
python manage.py migrate
python manage.py createsuperuser
Run the development server:
bash
Copier
Modifier
python manage.py runserver
📊 Future Improvements:
Add user authentication for ad submission.
Implement image upload previews.
Enhance ad filtering and search functionality.
