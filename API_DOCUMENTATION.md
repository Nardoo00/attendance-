# Attendance System API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### Home & Pages

#### Home Page
- **URL**: `/`
- **Method**: GET
- **Response**: HTML page with system overview and quick actions

#### Employees Page
- **URL**: `/employees`
- **Method**: GET
- **Response**: HTML page with employee list and management tools

#### Attendance Page
- **URL**: `/attendance`
- **Method**: GET
- **Query Parameters**:
  - `start_date` (optional): YYYY-MM-DD format
  - `end_date` (optional): YYYY-MM-DD format
- **Response**: HTML page with filtered attendance records

---

### Employee Management API

#### Add Employee
- **URL**: `/api/add-employee`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "employee_id": "EMP001",
    "email": "john@example.com",
    "department": "Engineering"
  }
  ```
- **Success Response** (200):
  ```json
  {
    "status": "success",
    "message": "Employee added successfully"
  }
  ```
- **Error Response** (400/500):
  ```json
  {
    "status": "error",
    "message": "Error description"
  }
  ```

#### Get All Employees
- **URL**: `/api/employees`
- **Method**: GET
- **Response** (200):
  ```json
  {
    "status": "success",
    "employees": [
      [1, "EMP001", "John Doe", "john@example.com", "Engineering", "2026-08-21T10:59:38Z"],
      [2, "EMP002", "Jane Smith", "jane@example.com", "HR", "2026-08-21T10:59:38Z"]
    ]
  }
  ```

---

### Facial Recognition API

#### Enroll Face
- **URL**: `/api/enroll-face/<employee_id>`
- **Method**: POST
- **Description**: Starts face enrollment process for an employee
- **Parameters**:
  - `employee_id` (required): Unique employee identifier
- **Response** (200):
  ```json
  {
    "status": "success",
    "message": "Face enrollment started"
  }
  ```
- **Error Response** (404):
  ```json
  {
    "status": "error",
    "message": "Employee not found"
  }
  ```
- **Process**:
  1. Camera window opens
  2. User faces camera
  3. Press SPACE to capture (5 samples needed)
  4. Press ESC to finish
  5. Face encoding stored in database

#### Start Recognition
- **URL**: `/api/start-recognition`
- **Method**: POST
- **Description**: Starts real-time facial recognition
- **Response** (200):
  ```json
  {
    "status": "success",
    "message": "Face recognition started"
  }
  ```
- **Process**:
  1. Camera window opens with live feed
  2. Detects faces in real-time
  3. Compares against known faces
  4. Records attendance for recognized employees
  5. Press 'q' to stop

---

### Attendance API

#### Get Attendance Records
- **URL**: `/api/attendance/<employee_id>`
- **Method**: GET
- **Query Parameters**:
  - `start_date` (optional): YYYY-MM-DD format
  - `end_date` (optional): YYYY-MM-DD format
- **Response** (200):
  ```json
  {
    "status": "success",
    "employee": {
      "id": "EMP001",
      "name": "John Doe",
      "department": "Engineering"
    },
    "records": [
      [1, "EMP001", "2026-08-21 09:00:00", "2026-08-21 17:30:00", "2026-08-21", "present"],
      [2, "EMP001", "2026-08-22 09:15:00", null, "2026-08-22", "present"]
    ]
  }
  ```
- **Error Response** (404):
  ```json
  {
    "status": "error",
    "message": "Employee not found"
  }
  ```

---

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |

---

## Data Models

### Employee
```
{
  "id": integer (auto-generated),
  "employee_id": string (unique),
  "name": string,
  "email": string (optional),
  "department": string (optional),
  "created_at": timestamp
}
```

### Attendance Record
```
{
  "id": integer (auto-generated),
  "employee_id": string,
  "check_in": timestamp,
  "check_out": timestamp (nullable),
  "date": date,
  "status": string ("present", "absent", "late"),
  "duration": duration (calculated)
}
```

### Face Encoding
```
{
  "id": integer (auto-generated),
  "employee_id": string,
  "encoding": binary (128-dimensional array),
  "created_at": timestamp
}
```

---

## Example Usage

### cURL Examples

**Add Employee**
```bash
curl -X POST http://localhost:5000/api/add-employee \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "employee_id": "EMP001",
    "email": "john@example.com",
    "department": "Engineering"
  }'
```

**Get Employees**
```bash
curl http://localhost:5000/api/employees
```

**Enroll Face**
```bash
curl -X POST http://localhost:5000/api/enroll-face/EMP001
```

**Start Recognition**
```bash
curl -X POST http://localhost:5000/api/start-recognition
```

**Get Attendance**
```bash
curl "http://localhost:5000/api/attendance/EMP001?start_date=2026-08-21&end_date=2026-08-22"
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding rate limiting middleware.

## Authentication

Currently no authentication is required. For production, implement JWT or session-based authentication.

## Error Handling

All errors return JSON responses with `status` and `message` fields for consistency.