import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ======================
# 1. DATABASE SETUP
# ======================
def init_db():
    conn = sqlite3.connect('fitness_tracker.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        weight_kg REAL,
        height_cm REAL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        type TEXT,
        duration_min INTEGER,
        calories_burned REAL,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nutrition (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        food TEXT,
        calories REAL,
        protein_g REAL,
        carbs_g REAL,
        fat_g REAL,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    return conn

# ======================
# 2. USER INPUT FUNCTIONS
# ======================
def add_user(conn, name, age, weight_kg, height_cm):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, age, weight_kg, height_cm) VALUES (?, ?, ?, ?)',
                   (name, age, weight_kg, height_cm))
    conn.commit()
    print(f"User {name} added successfully!")

def log_exercise(conn, user_id, exercise_type, duration_min, met_value):
    calories_burned = met_value * (get_user_weight(conn, user_id)) * (duration_min / 60)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO exercises (user_id, type, duration_min, calories_burned, date)
    VALUES (?, ?, ?, ?, ?)''', 
    (user_id, exercise_type, duration_min, calories_burned, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    print(f"Logged {exercise_type} exercise: {calories_burned:.2f} calories burned!")

def log_nutrition(conn, user_id, food, calories, protein_g, carbs_g, fat_g):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO nutrition (user_id, food, calories, protein_g, carbs_g, fat_g, date)
    VALUES (?, ?, ?, ?, ?, ?, ?)''',
    (user_id, food, calories, protein_g, carbs_g, fat_g, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    print(f"Logged {food} with {calories} calories")

# ======================
# 3. ANALYSIS FUNCTIONS
# ======================
def get_user_weight(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT weight_kg FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()[0]

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def get_weekly_summary(conn, user_id):
    # Load data into pandas
    exercises = pd.read_sql('SELECT * FROM exercises WHERE user_id = ?', conn, params=(user_id,))
    nutrition = pd.read_sql('SELECT * FROM nutrition WHERE user_id = ?', conn, params=(user_id,))
    
    # Process data
    exercises['date'] = pd.to_datetime(exercises['date'])
    nutrition['date'] = pd.to_datetime(nutrition['date'])
    
    weekly_exercise = exercises.resample('W', on='date')['calories_burned'].sum()
    weekly_nutrition = nutrition.resample('W', on='date')['calories'].sum()
    
    return weekly_exercise, weekly_nutrition

# ======================
# 4. VISUALIZATION FUNCTIONS
# ======================
def plot_progress(conn, user_id):
    # Get user data
    cursor = conn.cursor()
    cursor.execute('SELECT weight_kg, height_cm FROM users WHERE id = ?', (user_id,))
    weight, height = cursor.fetchone()
    bmi = calculate_bmi(weight, height)
    
    # Plot BMI
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.bar(['Your BMI'], [bmi], color='skyblue')
    plt.axhline(y=25, color='red', linestyle='--', label='Healthy Threshold')
    plt.title('BMI Analysis')
    plt.ylabel('BMI')
    plt.legend()
    
    # Plot weekly calories
    weekly_exercise, weekly_nutrition = get_weekly_summary(conn, user_id)
    plt.subplot(1, 2, 2)
    weekly_exercise.plot(label='Calories Burned', marker='o')
    weekly_nutrition.plot(label='Calories Consumed', marker='o')
    plt.title('Weekly Calorie Balance')
    plt.ylabel('Calories')
    plt.legend()
    plt.tight_layout()
    plt.show()

# ======================
# MAIN EXECUTION
# ======================
if __name__ == "__main__":
    conn = init_db()
    
    # Demo usage
    add_user(conn, "John Doe", 30, 70.5, 175)
    
    # Log activities (MET values: Running=7, Swimming=6, Cycling=5)
    log_exercise(conn, 1, "Running", 30, 7)
    log_exercise(conn, 1, "Swimming", 45, 6)
    
    # Log nutrition
    log_nutrition(conn, 1, "Chicken Salad", 350, 30, 20, 15)
    log_nutrition(conn, 1, "Protein Shake", 250, 25, 10, 5)
    
    # Generate visualizations
    plot_progress(conn, 1)
    
    conn.close()