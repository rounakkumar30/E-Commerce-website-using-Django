# 🛒 Django E-Commerce Website  

## 📌 Project Overview  
This is a **feature-rich e-commerce website** built using Django, allowing users to **register, verify their email, shop, manage profiles, and recover passwords securely**.  

## 🚀 Features  

### 🔐 **Authentication & User Management**  
- ✅ **Email Verification** – Users must verify their email before logging in.  
- ✅ **Secure Login & Logout** – Password hashing ensures security.  
- ✅ **Forgot Password** – Users can reset their password via email verification.  
- ✅ **Profile Management** – Edit profile details, change password, or delete account.  

### 🛍️ **Shopping & Order Features**  
- 🛒 **Product Listings** – Users can browse and view product details.  
- 🛍️ **Add to Cart** – Easily add/remove items before checkout.   

### 🎛️ **Admin Panel**  
- 🔧 **Manage users, products, orders, and more**.  
- 🔑 **Secure Django admin authentication**.  

### 📱 **Responsive Design**  
- 📲 **Optimized for desktop, tablet, and mobile devices**.  

---

## ⚙️ Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone [your_github_repo_link]
cd ecommerce-django


## ⚙️ Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone [your_github_repo_link]
cd ecommerce-django
```

### 2️⃣ Create a Virtual Environment  
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables  
Create a `.env` file in the root directory and add:  
```ini
SECRET_KEY=your_generated_secret_key
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_app_password
```

> 🔹 **Generate a SECRET_KEY** using:  
```python
import secrets
print(secrets.token_urlsafe(50))
```

> 🔹 **Use an App Password** instead of your actual email password for security.  

### 5️⃣ Apply Migrations  
```bash
python manage.py migrate
```

### 6️⃣ Create a Superuser (Admin Panel Access)  
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the Server  
```bash
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.  

---

## 🛠 Tech Stack  
- **Backend:** Django, SQLite/PostgreSQL  
- **Frontend:** HTML, CSS, Bootstrap  
- **Authentication:** Django Auth, Email Verification  

---

## 🤝 Contribution  
Feel free to **fork** the repository, create a **feature branch**, and submit a **pull request**!  

📌 **GitHub Repository:** https://github.com/rounakkumar30/E-Commerce-website-using-Django.git 

---

## 📩 Contact  
🔹 **Author:** Rounak Kumar  
🔹 **LinkedIn:** https://www.linkedin.com/in/rounakkumar30/  
🔹 **Email:** rounakverma30march@gmail.com  

---

### ⭐ **If you like this project, don't forget to give it a star!** ⭐  

#Django #Ecommerce #WebDevelopment #Python #Authentication #CyberSecurity #OpenSource 🚀
```

This is **GitHub-ready** with proper formatting, syntax highlighting, and clickable links. Just replace **[your_github_repo_link]** and **your social/contact info**, and you're good to go! 🚀
