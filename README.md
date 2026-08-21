# 👤 Facial Recognition Attendance System

A modern, intelligent attendance system that uses facial recognition technology to automatically track employee attendance. Built with Python, Flask, OpenCV, and SQLite.

## 🌟 Features

- **Real-time Facial Recognition**: Automatically detects and recognizes faces from your webcam
- **Built-in SQLite Database**: Stores employee data, face encodings, and attendance records
- **Employee Management**: Add, view, and manage employee profiles
- **Face Enrollment**: Capture and store facial data for each employee
- **Attendance Tracking**: Automatic check-in/check-out recording
- **Attendance Reports**: View attendance history with date filtering
- **Web Interface**: User-friendly Flask-based dashboard
- **Multi-user Support**: Handle multiple employees simultaneously

## 📋 System Architecture

```
attendance-system/
├── app.py                      # Flask web application
├── database.py                 # SQLite database management
├── face_recognition_module.py  # Facial recognition logic
├── requirements.txt            # Project dependencies
├── attendance.db              # SQLite database (auto-created)
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── employees.html         # Employee management
    └── attendance.html        # Attendance records
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Webcam/Camera
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nardoo00/attendance-.git
   cd attendance-
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   Open your browser and navigate to: `http://localhost:5000`

## 📖 Usage Guide

### 1. Add Employees

1. Go to **Employees** page
2. Click **+ Add New Employee**
3. Fill in employee details:
   - Full Name
   - Employee ID (unique)
   - Email (optional)
   - Department (optional)
4. Click **Add Employee**

### 2. Enroll Facial Data

1. In **Employees** page, find the employee
2. Click **Enroll Face** button
3. A camera window will open
4. Look at the camera
5. Press SPACE to capture (need 5 samples)
6. Press ESC when done

### 3. Start Recognition

1. Go to **Home** page
2. Click **Start Recognition** button
3. A live camera feed will open
4. Employees will be automatically recognized and attendance recorded
5. Press 'q' to stop

### 4. View Attendance Records

1. Go to **Attendance Records** page
2. Select date range
3. Click **Filter** to view records
4. See employee names, check-in/out times, and status

## 🗄️ Database Structure

### Employees Table
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    employee_id TEXT UNIQUE NOT NULL,
    email TEXT,
    department TEXT,
    created_at TIMESTAMP
)
```

### Face Encodings Table
```sql
CREATE TABLE face_encodings (
    id INTEGER PRIMARY KEY,
    employee_id TEXT NOT NULL,
    encoding BLOB NOT NULL,
    created_at TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
)
```

### Attendance Table
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    employee_id TEXT NOT NULL,
    check_in TIMESTAMP,
    check_out TIMESTAMP,
    date DATE,
    status TEXT DEFAULT 'present',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
)
```

## 🔌 API Endpoints

### Employee Management
- **POST** `/api/add-employee` - Add new employee
- **GET** `/api/employees` - Get all employees

### Facial Recognition
- **POST** `/api/enroll-face/<employee_id>` - Enroll employee face
- **POST** `/api/start-recognition` - Start real-time recognition

### Attendance
- **GET** `/api/attendance/<employee_id>` - Get employee attendance

### Web Pages
- **GET** `/` - Home page
- **GET** `/employees` - Employee management
- **GET** `/attendance` - Attendance records

## 🎛️ Configuration

Modify these settings in `face_recognition_module.py`:

```python
self.tolerance = 0.6  # Face matching tolerance (lower = stricter)
num_samples = 5       # Number of face samples during enrollment
```

## 🐛 Troubleshooting

### Camera not working
- Ensure camera is connected and not in use by another application
- Check camera permissions
- Try: `cv2.VideoCapture(1)` if using external camera

### Face not recognized
- Ensure good lighting conditions
- Capture faces from different angles during enrollment
- Lower the `tolerance` value for stricter matching

### Database errors
- Delete `attendance.db` to reset database
- Ensure you have write permissions in project folder

### Module import errors
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📊 Performance Tips

1. **Better Recognition**: Enroll faces in various lighting conditions
2. **Speed**: System processes at 0.25x resolution for faster recognition
3. **Accuracy**: Use high-quality camera and well-lit environment
4. **Database**: Regularly backup `attendance.db`

## 🔒 Security Considerations

- Face encodings are stored as binary data in the database
- Sensitive employee data should be protected
- Use HTTPS in production environment
- Implement user authentication for web interface
- Regularly backup the database

## 📦 Dependencies

- **opencv-python**: Computer vision and camera handling
- **face-recognition**: Deep learning face detection and recognition
- **numpy**: Numerical computing for face encodings
- **flask**: Web framework
- **pillow**: Image processing
- **scipy**: Scientific computing

## 🚀 Future Enhancements

- [ ] User authentication and login
- [ ] Export attendance reports to CSV/PDF
- [ ] Email notifications for check-ins
- [ ] Mobile app integration
- [ ] Multiple camera support
- [ ] Liveness detection (anti-spoofing)
- [ ] Advanced analytics and dashboards
- [ ] Database backup automation
- [ ] Multi-language support

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by **Nardoo00**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for automated attendance tracking**