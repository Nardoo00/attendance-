from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (
    init_database, add_employee, get_employee, get_all_employees,
    get_all_attendance, record_attendance, get_attendance_record
)
from face_recognition_module import FacialRecognitionSystem
from datetime import datetime, timedelta
import threading

app = Flask(__name__)
frs = FacialRecognitionSystem()

@app.route('/')
def index():
    """Home page"""
    employees = get_all_employees()
    return render_template('index.html', employees=employees)

@app.route('/employees')
def employees_page():
    """Employee management page"""
    employees = get_all_employees()
    return render_template('employees.html', employees=employees)

@app.route('/attendance')
def attendance_page():
    """Attendance records page"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    records = get_all_attendance(start_date, end_date)
    
    return render_template('attendance.html', 
                         records=records, 
                         start_date=start_date, 
                         end_date=end_date)

@app.route('/api/add-employee', methods=['POST'])
def add_employee_api():
    """API endpoint to add employee"""
    data = request.json
    
    try:
        result = add_employee(
            data['name'],
            data['employee_id'],
            data.get('email', ''),
            data.get('department', '')
        )
        
        if result:
            return jsonify({'status': 'success', 'message': 'Employee added successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Employee ID already exists'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/enroll-face/<employee_id>', methods=['POST'])
def enroll_face_api(employee_id):
    """API endpoint to enroll face for employee"""
    employee = get_employee(employee_id)
    
    if not employee:
        return jsonify({'status': 'error', 'message': 'Employee not found'}), 404
    
    # Start face enrollment in a separate thread
    thread = threading.Thread(target=frs.capture_face_for_enrollment, args=(employee_id,))
    thread.start()
    
    return jsonify({'status': 'success', 'message': 'Face enrollment started'})

@app.route('/api/start-recognition', methods=['POST'])
def start_recognition_api():
    """API endpoint to start real-time face recognition"""
    # Start recognition in a separate thread
    thread = threading.Thread(target=frs.recognize_face_from_camera)
    thread.start()
    
    return jsonify({'status': 'success', 'message': 'Face recognition started'})

@app.route('/api/attendance/<employee_id>', methods=['GET'])
def get_attendance_api(employee_id):
    """API endpoint to get attendance records for an employee"""
    employee = get_employee(employee_id)
    
    if not employee:
        return jsonify({'status': 'error', 'message': 'Employee not found'}), 404
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    records = get_all_attendance(start_date, end_date)
    emp_records = [r for r in records if r[1] == employee_id]
    
    return jsonify({
        'status': 'success',
        'employee': {
            'id': employee[1],
            'name': employee[2],
            'department': employee[4]
        },
        'records': emp_records
    })

@app.route('/api/employees', methods=['GET'])
def get_employees_api():
    """API endpoint to get all employees"""
    employees = get_all_employees()
    return jsonify({
        'status': 'success',
        'employees': employees
    })

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)