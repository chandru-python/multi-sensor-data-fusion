import numpy as np
import cv2
import matplotlib.pyplot as plt


# -----------------------------
# FILE PATHS
# -----------------------------

image_path = "dataset/camera/0000000000.png"
lidar_path = "dataset/lidar/0000000000.bin"

calib_velo_to_cam = "dataset/calibration/calib_velo_to_cam.txt"
calib_cam_to_cam = "dataset/calibration/calib_cam_to_cam.txt"


# -----------------------------
# READ IMAGE
# -----------------------------

img = cv2.imread(image_path)

if img is None:
    print("Image not found!")
    exit()

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# -----------------------------
# READ LIDAR
# -----------------------------

points = np.fromfile(lidar_path, dtype=np.float32).reshape(-1,4)

# remove intensity
points = points[:, :3]


# -----------------------------
# LOAD CALIBRATION
# -----------------------------

def read_calib(file):

    data = {}

    with open(file, 'r') as f:

        for line in f:

            if ':' not in line:
                continue

            key, value = line.split(':', 1)

            try:
                nums = [float(x) for x in value.split()]
                data[key.strip()] = np.array(nums)

            except:
                # skip unwanted lines
                pass

    return data



velo_calib = read_calib(calib_velo_to_cam)
cam_calib = read_calib(calib_cam_to_cam)


# Velodyne → Camera matrix
R = velo_calib['R'].reshape(3,3)
T = velo_calib['T'].reshape(3,1)

Tr = np.hstack((R, T))
Tr = np.vstack((Tr, [0,0,0,1]))


# Projection matrix
P = cam_calib['P_rect_02'].reshape(3,4)


# -----------------------------
# CONVERT TO HOMOGENEOUS
# -----------------------------

points_hom = np.hstack((points, np.ones((points.shape[0],1))))


# -----------------------------
# PROJECT LIDAR TO CAMERA
# -----------------------------

cam_points = Tr @ points_hom.T
cam_points = cam_points[:3,:]

# keep only front points
mask = cam_points[2,:] > 0
cam_points = cam_points[:, mask]


img_pts = P @ np.vstack((cam_points, np.ones((1, cam_points.shape[1]))))
img_pts /= img_pts[2,:]


u = img_pts[0,:].astype(int)
v = img_pts[1,:].astype(int)

depth = cam_points[2,:]


# -----------------------------
# DRAW POINTS
# -----------------------------

for i in range(len(u)):

    if 0 <= u[i] < img.shape[1] and 0 <= v[i] < img.shape[0]:

        # color based on depth
        color = plt.cm.jet(depth[i] / 50)[:3]
        color = tuple(int(c*255) for c in color)

        cv2.circle(img, (u[i], v[i]), 1, color, -1)


plt.figure(figsize=(12,6))
plt.imshow(img)
plt.title("LiDAR projected on camera")
plt.axis("off")
plt.show()
