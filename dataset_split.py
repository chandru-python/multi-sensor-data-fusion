import os
import shutil


# source dataset folder
source = "dataset1"

# destination folder
destination = "dataset2"


# create folders if not present
os.makedirs(destination, exist_ok=True)
os.makedirs(os.path.join(destination, "camera"), exist_ok=True)
os.makedirs(os.path.join(destination, "lidar"), exist_ok=True)
os.makedirs(os.path.join(destination, "imu"), exist_ok=True)
os.makedirs(os.path.join(destination, "calibration"), exist_ok=True)


# -----------------------------
# CAMERA FILES
# -----------------------------
camera_src = os.path.join(source, "image_02", "data")
camera_dst = os.path.join(destination, "camera")

if os.path.exists(camera_src):

    for file in os.listdir(camera_src):
        shutil.copy(os.path.join(camera_src, file), camera_dst)

    print("Camera files copied successfully!")

else:
    print("Camera folder not found.")



# -----------------------------
# LIDAR FILES
# -----------------------------
lidar_src = os.path.join(source, "velodyne_points", "data")
lidar_dst = os.path.join(destination, "lidar")

if os.path.exists(lidar_src):

    for file in os.listdir(lidar_src):
        shutil.copy(os.path.join(lidar_src, file), lidar_dst)

    print("LiDAR files copied successfully!")

else:
    print("LiDAR folder not found.")



# -----------------------------
# IMU FILES (optional)
# -----------------------------
imu_src = os.path.join(source, "oxts", "data")
imu_dst = os.path.join(destination, "imu")

if os.path.exists(imu_src):

    for file in os.listdir(imu_src):
        shutil.copy(os.path.join(imu_src, file), imu_dst)

    print("IMU files copied successfully!")

else:
    print("IMU folder not found.")



# -----------------------------
# CALIBRATION FILES
# -----------------------------
calib_src = os.path.join(source, "calibration_1")
calib_dst = os.path.join(destination, "calibration")

if os.path.exists(calib_src):

    for file in os.listdir(calib_src):
        shutil.copy(os.path.join(calib_src, file), calib_dst)

    print("Calibration files copied successfully!")

else:
    print("Calibration folder not found.")


print("\nDataset organized!")
