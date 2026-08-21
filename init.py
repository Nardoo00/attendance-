#!/usr/bin/env python
"""
Attendance System Initialization Script
Run this script to set up the system for the first time
"""

import os
from database import init_database

def main():
    print("\n" + "="*50)
    print("  Facial Recognition Attendance System")
    print("  Initialization Script")
    print("="*50 + "\n")
    
    print("[1/3] Creating database...")
    try:
        init_database()
        print("✓ Database initialized successfully\n")
    except Exception as e:
        print(f"✗ Error creating database: {e}\n")
        return
    
    print("[2/3] Checking dependencies...")
    try:
        import cv2
        import face_recognition
        import flask
        import numpy
        print("✓ All dependencies installed\n")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("  Run: pip install -r requirements.txt\n")
        return
    
    print("[3/3] System configuration...")
    print("✓ System ready to use\n")
    
    print("="*50)
    print("  Setup Complete!")
    print("="*50)
    print("\nNext steps:")
    print("  1. Run: python app.py")
    print("  2. Open: http://localhost:5000")
    print("  3. Add employees and enroll faces")
    print("  4. Start facial recognition\n")

if __name__ == '__main__':
    main()