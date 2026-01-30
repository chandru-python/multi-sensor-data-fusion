import numpy as np
import cv2
import os
from filterpy.kalman import KalmanFilter


# =============================
# RELATIVE PATHS
# =============================

camera_folder = "dataset1/camera"
lidar_folder = "dataset1/lidar"

calib_velo_to_cam = "dataset1/calibration/calib_velo_to_cam.txt"
calib_cam_to_cam = "dataset1/calibration/calib_cam_to_cam.txt"


# =============================
# READ CALIBRATION
# =============================

def read_calib(file):
    data = {}

    with open(file, 'r') as f:
        for line in f.readlines():

            if ':' not in line:
                continue

            key, value = line.split(':', 1)

            try:
                data[key.strip()] = np.array([float(x) for x in value.split()])
            except:
                continue

    return data


velo_calib = read_calib(calib_velo_to_cam)
cam_calib = read_calib(calib_cam_to_cam)

R = velo_calib['R'].reshape(3,3)
T = velo_calib['T'].reshape(3,1)

Tr_velo_to_cam = np.vstack((np.hstack((R,T)), [0,0,0,1]))
P_rect = cam_calib['P_rect_02'].reshape(3,4)


# =============================
# KALMAN FILTER
# =============================

kf = KalmanFilter(dim_x=2, dim_z=1)

# State = [distance, velocity]
kf.x = np.array([[10.],
                 [0.]])

kf.F = np.array([[1., 1.],
                 [0., 1.]])

kf.H = np.array([[1., 0.]])

kf.P *= 10
kf.R = 3
kf.Q = np.array([[0.5, 0],
                 [0, 0.5]])


# =============================
# LOAD FILES SAFELY
# =============================

camera_files = sorted(os.listdir(camera_folder))
lidar_files = sorted(os.listdir(lidar_folder))

print("Camera Frames:", len(camera_files))
print("LiDAR Frames:", len(lidar_files))

num_frames = min(len(camera_files), len(lidar_files))

if num_frames == 0:
    print("❌ No data found. Check dataset paths.")
    exit()

print("Processing Frames:", num_frames)


# =============================
# MAIN LOOP
# =============================

for i in range(num_frames):

    img_path = os.path.join(camera_folder, camera_files[i])
    lidar_path = os.path.join(lidar_folder, lidar_files[i])

    # Load Image
    img = cv2.imread(img_path)

    if img is None:
        print("Skipping bad image:", img_path)
        continue


    # Load LiDAR
    points = np.fromfile(lidar_path, dtype=np.float32).reshape(-1,4)
    points = points[:, :3]


    # Convert to Homogeneous
    points_hom = np.hstack((points, np.ones((points.shape[0],1))))

    # Transform LiDAR -> Camera
    cam_points = Tr_velo_to_cam @ points_hom.T
    cam_points = cam_points[:3,:]

    # Keep only points in front
    mask = cam_points[2,:] > 0
    cam_points = cam_points[:,mask]

    # Project onto image
    img_pts = P_rect @ np.vstack((cam_points, np.ones((1,cam_points.shape[1]))))
    img_pts /= img_pts[2,:]

    u = img_pts[0,:].astype(int)
    v = img_pts[1,:].astype(int)

    depth = cam_points[2,:]
    height = cam_points[1,:]


    # =============================
    # DRAW LIDAR POINTS
    # =============================

    for j in range(len(u)):

        if 0 <= u[j] < img.shape[1] and 0 <= v[j] < img.shape[0]:

            d = depth[j]

            if d < 10:
                color = (0,0,255)     # Red = Very Close
            elif d < 20:
                color = (0,165,255)   # Orange = Medium
            else:
                color = (255,0,0)     # Blue = Far

            cv2.circle(img, (u[j], v[j]), 1, color, -1)


    # =============================
    # ROBUST DISTANCE ESTIMATION
    # =============================

    valid = (depth > 5) & (depth < 50) & (height > -1.2)

    front = depth[valid]

    if len(front) > 30:

        measurement = np.percentile(front, 5)

        # Kalman Predict
        kf.predict()

        # Kalman Update
        kf.update(measurement)

        tracked_distance = kf.x[0][0]

        cv2.putText(img,
                    f"Tracked Distance: {tracked_distance:.2f} m",
                    (40,60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0,255,0),
                    3)


    # =============================
    # DISPLAY
    # =============================

    cv2.imshow("RESEARCH LEVEL SENSOR FUSION", img)

    # ESC to Exit
    if cv2.waitKey(30) & 0xFF == 27:
        break


cv2.destroyAllWindows()
