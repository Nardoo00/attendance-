import sqlite3
from datetime import datetime
import os

DB_PATH = 'attendance.db'

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            email TEXT,
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create attendance records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            check_in TIMESTAMP,
            check_out TIMESTAMP,
            date DATE,
            status TEXT DEFAULT 'present',
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_employee(name, employee_id, email, department):
    """Add a new employee to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO employees (name, employee_id, email, department)
            VALUES (?, ?, ?, ?)
        ''', (name, employee_id, email, department))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_employee(employee_id):
    """Retrieve employee information"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    
    return employee

def record_attendance(employee_id, check_in=True):
    """Record attendance check-in or check-out"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    if check_in:
        cursor.execute('''
            INSERT INTO attendance (employee_id, check_in, date, status)
            VALUES (?, ?, ?, ?)
        ''', (employee_id, datetime.now(), today, 'present'))
    else:
        cursor.execute('''
            UPDATE attendance 
            SET check_out = ? 
            WHERE employee_id = ? AND date = ? AND check_out IS NULL
        ''', (datetime.now(), employee_id, today))
    
    conn.commit()
    conn.close()

def get_attendance_record(employee_id, date):
    """Get attendance record for a specific date"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM attendance 
        WHERE employee_id = ? AND date = ?
    ''', (employee_id, date))
    record = cursor.fetchone()
    conn.close()
    
    return record

def get_all_attendance(start_date=None, end_date=None):
    """Get all attendance records within a date range"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if start_date and end_date:
        cursor.execute('''
            SELECT a.*, e.name FROM attendance a
            JOIN employees e ON a.employee_id = e.employee_id
            WHERE a.date BETWEEN ? AND ?
            ORDER BY a.date DESC
        ''', (start_date, end_date))
    else:
        cursor.execute('''
            SELECT a.*, e.name FROM attendance a
            JOIN employees e ON a.employee_id = e.employee_id
            ORDER BY a.date DESC
        ''')
    
    records = cursor.fetchall()
    conn.close()
    
    return records

def get_all_employees():
    """Get all employees"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()
    
    return employees
