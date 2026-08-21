import cv2
import numpy as np
from database import record_attendance, get_employee, get_all_employees
from datetime import datetime
import pickle
import os

class FacialRecognitionSystem:
    def __init__(self):
        # Use pre-trained Haar Cascade classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_face_names = []
        self.model_path = 'face_model.yml'
        self.labels_path = 'face_labels.pkl'
        self.faces = []
        self.labels = []
        self.load_model()
        
    def load_model(self):
        """Load the trained face recognition model"""
        if os.path.exists(self.model_path) and os.path.exists(self.labels_path):
            try:
                self.recognizer.read(self.model_path)
                with open(self.labels_path, 'rb') as f:
                    self.known_face_names = pickle.load(f)
                print(f"✓ Model loaded with {len(self.known_face_names)} employees")
            except Exception as e:
                print(f"Error loading model: {e}")
        
    def save_model(self):
        """Save the trained model"""
        try:
            self.recognizer.write(self.model_path)
            with open(self.labels_path, 'wb') as f:
                pickle.dump(self.known_face_names, f)
            print("✓ Model saved successfully")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def capture_face_for_enrollment(self, employee_id, num_samples=30):
        """Capture facial images for a new employee using OpenCV only"""
        employee = get_employee(employee_id)
        if not employee:
            print(f"Employee {employee_id} not found")
            return False
        
        cap = cv2.VideoCapture(0)
        captured_count = 0
        faces = []
        
        print(f"\nStarting face capture for: {employee[2]}")
        print(f"Please look at the camera. We will capture {num_samples} face samples.")
        print("Press SPACE to capture, ESC to exit\n")
        
        while captured_count < num_samples:
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to capture image")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Draw rectangles around detected faces
            for (x, y, w, h) in detected_faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Display info
            cv2.putText(frame, f"Samples: {captured_count}/{num_samples}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "SPACE=Capture, ESC=Exit", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
            
            cv2.imshow('Face Enrollment', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # SPACE key
                if len(detected_faces) > 0:
                    # Use the largest detected face
                    x, y, w, h = max(detected_faces, key=lambda f: f[2]*f[3])
                    face_roi = gray[y:y+h, x:x+w]
                    faces.append(face_roi)
                    captured_count += 1
                    print(f"  ✓ Sample {captured_count} captured")
                else:
                    print("  ✗ No face detected. Please try again.")
            elif key == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if len(faces) > 0:
            # Add to training data
            emp_label = len(self.known_face_names)
            self.known_face_names.append(employee_id)
            
            for face in faces:
                self.faces.append(face)
                self.labels.append(emp_label)
            
            # Train the model
            if len(self.faces) > 0:
                self.recognizer.train(self.faces, np.array(self.labels))
                self.save_model()
                print(f"\n✓ Face training completed for {employee[2]}")
                return True
        else:
            print("✗ Failed to capture faces")
            return False
    
    def recognize_face_from_camera(self):
        """Real-time face recognition from camera"""
        if len(self.known_face_names) == 0:
            print("\n⚠ No faces enrolled yet. Please enroll employees first.")
            return
        
        cap = cv2.VideoCapture(0)
        recognized_today = set()
        confidence_threshold = 70  # Lower is better match (0-100)
        
        print("\n" + "="*50)
        print("  Face Recognition Started")
        print("  Press 'q' to quit")
        print("="*50 + "\n")
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected_faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            frame_count += 1
            
            for (x, y, w, h) in detected_faces:
                face_roi = gray[y:y+h, x:x+w]
                
                # Only recognize every 5 frames to reduce processing
                if frame_count % 5 == 0:
                    try:
                        label, confidence = self.recognizer.predict(face_roi)
                        
                        if confidence < confidence_threshold and label < len(self.known_face_names):
                            emp_id = self.known_face_names[label]
                            employee = get_employee(emp_id)
                            name = employee[2] if employee else "Unknown"
                            color = (0, 255, 0)  # Green
                            
                            # Record attendance
                            if emp_id not in recognized_today:
                                record_attendance(emp_id, check_in=True)
                                recognized_today.add(emp_id)
                                print(f"✓ Attendance recorded: {name} ({emp_id})")
                        else:
                            name = "Unknown"
                            color = (0, 0, 255)  # Red
                    except Exception as e:
                        name = "Unknown"
                        color = (0, 0, 255)
                else:
                    name = "Processing..."
                    color = (255, 165, 0)  # Orange
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
                cv2.putText(frame, name, (x+6, y-10), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Attendance System - Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("\n" + "="*50)
        print("  Recognition stopped")
        print("="*50 + "\n")
