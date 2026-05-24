✅ Task Manager API

A full-stack Task Management web application that helps users manage daily tasks efficiently with secure authentication and CRUD operations.

✨ What it does

Register and login securely
Create daily tasks
View all tasks
Mark tasks as completed
Delete tasks instantly
Stores user and task data in SQLite database
JWT-based authentication system

🔥 Features

Secure password hashing using bcrypt
Token-based authentication
FastAPI REST APIs
Responsive frontend UI
CRUD task operations
Frontend connected with deployed backend

🛠️ Tech Stack

Backend: FastAPI + SQLAlchemy + SQLite
Authentication: JWT + Passlib + bcrypt
Frontend: HTML + CSS + JavaScript
Deployment: Render + Vercel

📂 Project Structure

task-manager/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│
└── README.md

🚀 Run Locally

Backend

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend

Open index.html using Live Server

🌐 Deployment

Frontend deployed on Vercel
Backend deployed on Render

📌 Future Improvements

Task deadlines and reminders
Dark mode UI
Task categories
Cloud database integration
Drag and drop task management

👩‍💻 Author

Deerthika J
