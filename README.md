# About the project
This is a backend-focused web application built with django, where users can track their daily habits and see their progress over time.

I built this project to practice:
-> backend logic
-> working with databases
-> structuring a real web application
-> writing clean and readable code

The main focus was functionality and logic, not UI design.

# What the app does
- Users can register and log in
- Users can create habits (for example: reading, drinking water, etc.)
- Each habit can be marked as done for a specific day
- The app tracks: 
   - daily completion
   - weekly progress (lasy 7 days)
   - current streak (consecutive days)

# Tech stack
- Python
- Django
- Django ORM
- HTML with Django templates
- SQLite (for development)

# How it works
Habits and daily logs
- each habit is stored separately from its daily completion

- for daily tracking, I use a HabtLog model that stores: the habit, the date, whetes it was completed or not

- this makes it easy to: 
   - check is a habit was done on a specific day
   - calculate weekly progress
   -calculate streaks

Streak calculation
- the streak is calculated dynamically:
   - check the last 7 days
   - start from today and go backwards
   - count how many consecutive days the habit was completed
   - the streak stops at the first day that was not completed

- I chose this approach instead of storing the streak in the database to keep the data consistent.

Weekly summary
- for each habit, the dashboard shows:
   - how many days it was completed in the last 7 days
   - the completion percentage
   - a simple visual indicator (🔥 🙂 ❗)

- all calculations are done in the Django view using ORM queries.

Dashboard
- the dashboard shows:
   - all user habits
   - current streak for each habit
   - a table with daily completion for the last 7 days
   - a weekly summary per habit

- this helped me understand how to aggregate data and pass structured information to templates.

# Why I built it this way
- I wanted to focus on backend logic first
- I avoided overcomplicating the frontend
- I tried to keep the views readable and easy to follow
- I used Django ORM instead of raw SQL

# Possible improvements

- add a REST API (Django REST Framework)
- add tests
- improve performance with caching
- build a frontend with JavaScript


# How to run the project locally

git clone https://github.com/corinaalexandranecula-bit/daily-habit-tracker.git
cd daily-habit-tracker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver