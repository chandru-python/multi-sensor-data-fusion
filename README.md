🚗 Multi-Sensor Data Fusion for Self-Driving Cars
Using LiDAR, Camera, and Kalman Filter
📌 Project Overview

This project demonstrates an advanced perception system used in autonomous vehicles by combining data from multiple sensors — LiDAR and Camera — and applying a Kalman Filter to improve object tracking accuracy.

Sensor fusion helps reduce uncertainty from individual sensors and provides a more reliable understanding of the surrounding environment, which is critical for safe self-driving operations.

🎯 Objectives

Combine LiDAR and camera data for better object detection

Implement Kalman filtering for smooth and accurate tracking

Reduce noise and improve prediction accuracy

Simulate real-world autonomous driving perception

🧠 Technologies Used

Python

OpenCV

NumPy

Kalman Filter

Sensor Fusion Techniques

⚙️ How It Works

Camera Input captures visual information from the environment.

LiDAR Data provides depth and distance measurements.

Both sensor outputs are aligned and projected into a common coordinate system.

A Kalman Filter predicts object positions and corrects them using real-time measurements.

The final output shows stable and accurate object tracking.

📊 Output

(Add your image file name below — example:)

![Sensor Fusion Output](kalman.png)


👉 This helps recruiters instantly see your result.

▶️ How to Run the Project
✅ Step 1 — Clone Repository
git clone https://github.com/chandru-python/Multi-Sensor-Data-Fusion-for-Self-Driving-Cars-using-LiDAR-Camera-and-Kalman-Filter.git

✅ Step 2 — Install Requirements
pip install -r requirements.txt

✅ Step 3 — Run the Script
python realtime_time_sensor_fusion_kalman.py

📁 Project Structure
fusion/
│
├── realtime_time_sensor_fusion_kalman.py
├── lidar_camera_projection.py
├── dataset_split.py
├── requirements.txt
└── kalman.png
# NOTE : Download dataset from KITTI (https://www.cvlibs.net/datasets/kitti/) 

🚀 Future Improvements

Integrate Deep Learning-based object detection (YOLO / Faster R-CNN)

Optimize for real-time performance

Deploy on edge devices

Add radar sensor fusion

Build a live dashboard visualization

💡 Why This Project Matters

Sensor fusion is a core technology in autonomous vehicles used by modern intelligent transportation systems.

This project demonstrates practical knowledge of:

✅ Computer Vision
✅ State Estimation
✅ Robotics Concepts
✅ Real-time data processing

— skills highly valued in AI and autonomous systems roles.

👨‍💻 Author

Chandru
AI / ML Enthusiast | Computer Vision Developer

⭐ If you found this project useful, consider giving it a star!
