
# 📚 StudySwap

StudySwap is a web application that helps students share and find available study spots in real time. Users can share free study spaces, claim spots, and earn karma points based on activity.

---

## 🚀 Features

- 🔐 User authentication (login/signup)
- 📍 Share study spots with details
- 🙋 Claim available spots
- ⭐ Karma points system (gamification)
- 📊 User ranking system (Rookie, Hunter, Spot Master)
- 🎨 Responsive UI with HTML, CSS, and JavaScript

---

## 🛠️ Tech Stack

- FastAPI (Python backend)
- HTML, CSS, JavaScript (frontend)
- Jinja2 templates
- SQLAlchemy (database ORM)
- SQLite (default database)

---

## 📂 Project Structure
- main.py
- auth.py
- database.py
- models.py
- static/
- templates/
- requirements.txt
- Procfile


---

## ▶️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Maryam19122005/studyswap.git
cd studyswap

2. Create virtual environment
python -m venv venv
3. Activate virtual environment
venv\Scripts\activate   # Windows
4. Install dependencies
pip install -r requirements.txt
5. Run the server
uvicorn main:app --reload
6. Open in browser
http://127.0.0.1:8000
🌐 Deployment

This project is deployed using Render:

Start command:
uvicorn main:app --host 0.0.0.0 --port 10000




👤 Author
Maryam Sajjad Ahmed Awan 
GitHub: https://github.com/Maryam19122005


⭐ Future Improvements
PostgreSQL database support
Mobile app version
Real-time chat between students
Notifications system
Google login integration

---

 


