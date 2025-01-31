from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'progress.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for progress tracking (now includes week column)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)  # Week Number
    task_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), default="🔄")  # Default: In Progress

# Week-wise roadmap tasks
tasks_list = [
    # Week 1
    (1, "HTML5: Structure, Semantic Elements"),
    (1, "CSS3: Flexbox, Grid, Animations"),
    (1, "JavaScript Basics: ES6, DOM Manipulation"),
    (1, "Build a simple landing page & portfolio website"),
    
    # Week 2
    (2, "ES6+: Promises, Async/Await, Fetch API"),
    (2, "LocalStorage, SessionStorage"),
    (2, "JSON, APIs & HTTP Methods (GET, POST)"),
    (2, "Git & GitHub: Version Control, Branching"),
    (2, "Build a to-do app with local storage"),

    # Week 3
    (3, "React Basics: JSX, Components, Props"),
    (3, "State & Events Handling"),
    (3, "React Hooks (useState, useEffect)"),
    (3, "React Router (Navigation & Routing)"),
    (3, "Build a multi-page website using React Router"),

    # Week 4
    (4, "Context API & useReducer"),
    (4, "Handling Forms & Validation"),
    (4, "Fetching & Displaying API Data"),
    (4, "Responsive Design with Tailwind CSS"),
    (4, "Build a Weather App using OpenWeather API"),

    # Week 5
    (5, "Node.js Basics: Modules, FS, HTTP"),
    (5, "Express.js: Middleware, Routing, Error Handling"),
    (5, "Build a Basic REST API (CRUD with Express.js)"),

    # Week 6
    (6, "MongoDB + Mongoose: Models & CRUD Operations"),
    (6, "JWT Authentication & bcrypt.js"),
    (6, "RESTful API Design & Postman Testing"),
    (6, "Build a User Authentication System"),

    # Week 7
    (7, "Fetch Data from Backend in React"),
    (7, "Redux Toolkit (State Management)"),
    (7, "File Upload (Multer), Image Storage"),
    (7, "Build a Full-Stack Blog App (MERN Stack)"),

    # Week 8
    (8, "Role-Based Access (Admin/User)"),
    (8, "Secure API (Helmet, CORS, Rate Limiting)"),
    (8, "Deploy Backend on Render/Vercel"),
    (8, "Deploy MongoDB on Atlas"),
    (8, "Build a Secure E-commerce Backend API"),

    # Week 9
    (9, "Product Listings, Cart Functionality"),
    (9, "Payment Gateway Integration (Stripe/Razorpay)"),
    (9, "User Dashboard & Admin Panel"),
    (9, "Build a Full-Stack E-commerce App (MERN)"),

    # Week 10
    (10, "WebSockets (Real-time Chat with Socket.io)"),
    (10, "Caching (Redis), Pagination, Lazy Loading"),
    (10, "Next.js for SSR & SEO"),
    (10, "Implement Dark Mode & Performance Optimization"),

    # Week 11
    (11, "CI/CD: GitHub Actions"),
    (11, "Docker & Kubernetes (Basics)"),
    (11, "Deploy Full-Stack App on Vercel/Netlify & AWS"),
    (11, "Build a Portfolio showcasing all projects"),

    # Week 12
    (12, "Solve 50+ DSA Questions (Frontend + Backend)"),
    (12, "Mock Interviews & System Design Basics"),
    (12, "Resume Building & Portfolio Completion"),
    (12, "Apply for Internships/Jobs & Freelancing")
]

# Initialize database and populate it with week-wise tasks
def initialize_db():
    with app.app_context():
        db.create_all()
        if Task.query.count() == 0:  # Populate only if empty
            for week, task in tasks_list:
                db.session.add(Task(week=week, task_name=task))
            db.session.commit()

# Route: Display progress tracking, grouped by weeks
@app.route('/')
def index():
    tasks_by_week = {}
    tasks = Task.query.all()
    for task in tasks:
        if task.week not in tasks_by_week:
            tasks_by_week[task.week] = []
        tasks_by_week[task.week].append(task)
    return render_template('index.html', tasks_by_week=tasks_by_week)

# Route: Update task status
@app.route('/update/<int:task_id>/<status>')
def update(task_id, status):
    task = Task.query.get(task_id)
    if task:
        task.status = status
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    initialize_db()  # Ensure database is initialized before running
    app.run(debug=True)