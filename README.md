SMART TRAFFIC MANAGEMENT SYSTEM

A desktop application that detects vehicles in uploaded traffic images and simulates a smart traffic light. The green signal time adjusts based on vehicle count using YOLOv8.

---

## FEATURES

* Admin login system
* Upload JPEG images
* Detects vehicles using YOLOv8
* Automatically adjusts green light time
* Simulates red, yellow, and green lights
* Progress bar to show detection steps
* Displays results with vehicle count and timing
* Saves processed images
* Logs activity and detection

---

## HOW IT WORKS

1. Admin logs in with username and password
2. Image with traffic is uploaded
3. App detects vehicles using a pre-trained model
4. Calculates green signal time based on count
5. Animates traffic light phases
6. Shows final result

---

## REQUIREMENTS

* Python 3.8 or newer
* OpenCV
* Ultralytics YOLOv8
* Tkinter (comes with most Python installations)

---

## HOW TO USE

1. Start the app
2. Login using admin credentials
3. Upload an image
4. Wait for vehicle detection
5. View light simulation and results

---

## FILES AND FOLDERS

* traffic\_app.py → Main application file
* green\_time\_signal.py → Green time logic
* vehicle\_count.txt → Latest count storage
* /images → Folder for saved images
* traffic\_app.log → Log file
* README.txt → This documentation

---

## LOGIN DETAILS

Username: admin
Password: traffic123

---

## NOTES

* Accepts only JPG or JPEG image formats
* YOLOv8 model file must be available as yolov8l.pt
* Detected output images are saved in the "images" folder

---

## FUTURE IMPROVEMENTS

* Video feed support
* Real-time webcam detection
* Save data to a database
* Multi-user login and analytics

---

## LICENSE

This project is licensed under the MIT License.

---

## CREDITS

* YOLOv8 by Ultralytics
* OpenCV for image processing
* Tkinter for the user interface

---


