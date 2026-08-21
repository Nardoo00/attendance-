# Attendance System Configuration

# Flask Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Database
DB_PATH = 'attendance.db'

# Face Recognition Settings
FACE_RECOGNITION_TOLERANCE = 0.6  # Lower = stricter matching
FACE_SAMPLES_FOR_ENROLLMENT = 5   # Number of face samples to capture
FACE_DETECTION_SCALE = 0.25       # Process at 0.25x resolution for speed

# Camera Settings
CAMERA_INDEX = 0                   # Default camera (0 = built-in)
CAMERA_RESOLUTION = (640, 480)     # Camera resolution
CAMERA_FPS = 30                    # Frames per second

# Attendance Settings
AUTO_CHECK_OUT_HOURS = 8           # Auto check-out after N hours
MIN_FACE_CONFIDENCE = 0.95         # Minimum confidence for recognition