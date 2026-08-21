import cv2
import face_recognition
import numpy as np
import pickle
from database import get_face_encoding, add_face_encoding, record_attendance, get_employee
from datetime import datetime

class FacialRecognitionSystem:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.known_face_encodings = []
        self.known_face_names = []
        self.tolerance = 0.6
        
    def capture_face_for_enrollment(self, employee_id, num_samples=5):
        """Capture facial images for a new employee"""
        cap = cv2.VideoCapture(0)
        captured_count = 0
        face_encodings = []
        
        print(f"Starting face capture for employee: {employee_id}")
        print(f"Please look at the camera. We will capture {num_samples} face samples.")
        
        while captured_count < num_samples:
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to capture image")
                break
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings_list = face_recognition.face_encodings(rgb_frame, face_locations)
            
            # Draw rectangles around faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Display info
            cv2.putText(frame, f"Samples captured: {captured_count}/{num_samples}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press SPACE to capture, ESC to exit", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
            
            cv2.imshow('Face Enrollment', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # SPACE key
                if len(face_encodings_list) > 0:
                    face_encodings.append(face_encodings_list[0])
                    captured_count += 1
                    print(f"Face sample {captured_count} captured")
                else:
                    print("No face detected. Please try again.")
            elif key == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if len(face_encodings) > 0:
            # Average the encodings
            face_encoding_avg = np.mean(face_encodings, axis=0)
            # Store in database
            add_face_encoding(employee_id, face_encoding_avg.tobytes())
            print(f"Face encoding stored successfully for {employee_id}")
            return True
        else:
            print("Failed to capture face samples")
            return False
    
    def recognize_face_from_camera(self):
        """Real-time face recognition from camera"""
        cap = cv2.VideoCapture(0)
        recognized_today = set()
        
        print("Starting face recognition system...")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find faces and encodings
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings_list = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            face_names = []
            face_distances_list = []
            
            for face_encoding in face_encodings_list:
                # Compare with database
                match_found = False
                employees = self._get_all_employees_with_faces()
                
                for emp_id, stored_encoding in employees:
                    if stored_encoding is None:
                        continue
                    
                    distance = face_recognition.face_distance([stored_encoding], face_encoding)
                    
                    if distance[0] < self.tolerance:
                        face_names.append(emp_id)
                        face_distances_list.append(distance[0])
                        match_found = True
                        
                        # Record attendance
                        if emp_id not in recognized_today:
                            record_attendance(emp_id, check_in=True)
                            recognized_today.add(emp_id)
                            employee = get_employee(emp_id)
                            print(f"✓ Attendance recorded for: {employee[2]} ({emp_id})")
                        break
                
                if not match_found:
                    face_names.append("Unknown")
                    face_distances_list.append(1.0)
            
            # Display results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Attendance System - Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def _get_all_employees_with_faces(self):
        """Get all employees with their face encodings"""
        from database import get_all_employees
        
        employees_with_faces = []
        employees = get_all_employees()
        
        for employee in employees:
            employee_id = employee[1]
            encoding_bytes = get_face_encoding(employee_id)
            
            if encoding_bytes:
                encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
                employees_with_faces.append((employee_id, encoding))
        
        return employees_with_faces