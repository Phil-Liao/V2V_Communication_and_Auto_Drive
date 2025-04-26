import cv2
import numpy as np
import pyapriltags as apriltag
import socket
import threading
import math

nickname = 'A'

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.68.50.32', 7777))

pose_BC = None

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message[:len(nickname)] != nickname:
                global pose_BC
                pose_BC = message
        except:
            # Close Connection When Error
            client.close()
            print("[DISCONNECTED] An error occured.")
            break

def pose_to_matrix(pose):
    """
    將 (x, y, theta)（其中 theta 為角度單位）轉換成 3x3 齊次變換矩陣
    """
    x, y, theta_deg = pose
    theta = math.radians(theta_deg)  # 角度轉弧度
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    return np.array([
        [cos_theta, -sin_theta, x],
        [sin_theta,  cos_theta, y],
        [0,         0,         1]
    ])

def matrix_to_pose(matrix):
    """
    從 3x3 齊次變換矩陣中提取 (x, y, theta)，其中 theta 為角度單位
    """
    x = matrix[0, 2]
    y = matrix[1, 2]
    theta = math.atan2(matrix[1, 0], matrix[0, 0])
    return (x, y, math.degrees(theta))  # 弧度轉角度

def compute_pose(pose_AB, pose_BC):
    """
    根據已知的 A->B 與 B->C 的變換，計算 A->C 的變換。
    輸入與輸出之角度皆為度。
    """
    T_AB = pose_to_matrix(pose_AB)
    T_BC = pose_to_matrix(pose_BC)
    # 從 A 到 C 的變換矩陣為 T_AC = T_AB * T_BC
    T_AC = np.dot(T_AB, T_BC)
    return matrix_to_pose(T_AC)

# 設定相機內參 (根據相機校正調整)
camera_matrix = np.array([[797.19922282, 0, 319.75614916],  # fx
                          [0, 801.8848903, 259.20202143],  # fy
                          [0, 0, 1]], dtype=np.float32)     # cx, cy
dist_coeffs = np.array([3.74005891e-02, -1.96034587e+00, -2.19501972e-03, 2.93313263e-03, 2.10149607e+01], dtype=np.float32) # 假設無畸變，若有請填入相機校正值

# 設定 AprilTag 大小 (單位：公尺)
tag_size = 0.045  # 10cm

# 初始化 AprilTag 偵測器
detector = apriltag.Detector(families='tag36h11')

receive_thread = threading.Thread(target=receive)
receive_thread.start()

# 開啟攝影機
cap = cv2.VideoCapture(0)  # 0 代表預設攝影機

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        client.close()
        break
    # 轉為灰階圖像（AprilTag 偵測器需要灰階輸入）
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 偵測 AprilTag
    detections = detector.detect(gray)
    for detection in detections:
        # 取得四個角點
        corners = np.array(detection.corners, dtype=np.float32)

        # 確保座標為整數，避免 OpenCV 錯誤
        for i in range(4):
            pt1 = tuple(map(int, corners[i]))  
            pt2 = tuple(map(int, corners[(i + 1) % 4]))  
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        # 設定 3D 物理世界座標（AprilTag 的四個角）
        tag_3d_points = np.array([
            [-tag_size / 2, -tag_size / 2, 0],  # 左上
            [ tag_size / 2, -tag_size / 2, 0],  # 右上
            [ tag_size / 2,  tag_size / 2, 0],  # 右下
            [-tag_size / 2,  tag_size / 2, 0]   # 左下
        ], dtype=np.float32)

        # 計算 3D 位置與旋轉資訊
        _, rvec, tvec = cv2.solvePnP(tag_3d_points, corners, camera_matrix, dist_coeffs)

        # 取得物品的 3D 位置
        x, y, z = tvec.flatten()

        # 轉換旋轉向量 (rvec) 為旋轉矩陣
        R, _ = cv2.Rodrigues(rvec)

        # 計算歐拉角 (Roll, Pitch, Yaw)
        sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
        singular = sy < 1e-6

        if not singular:
            roll = np.arctan2(R[2, 1], R[2, 2])  # X 軸旋轉 (Roll)
            pitch = np.arctan2(-R[2, 0], sy)     # Y 軸旋轉 (Pitch)
            yaw = np.arctan2(R[1, 0], R[0, 0])   # Z 軸旋轉 (Yaw)
        else:
            roll = np.arctan2(-R[1, 2], R[1, 1])
            pitch = np.arctan2(-R[2, 0], sy)
            yaw = 0

        # 轉換弧度為角度
        roll = np.degrees(roll)
        pitch = np.degrees(pitch)
        yaw = np.degrees(yaw)

        # 顯示位置與轉向資訊
        text1 = f"X: {x*100:.0f} cm, Y: {y*100:.0f} cm, Z: {z*100:.0f} cm"
        text2 = f"Roll: {roll:.2f} deg, Pitch: {pitch:.2f} deg, Yaw: {yaw:.2f} deg"

        cv2.putText(frame, text1, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, text2, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    if pose_BC:
        try:
            start = pose_BC.find("(") + 1  # Find the opening parenthesis and move past it
            end = pose_BC.find(")")  # Find the closing parenthesis
            pose_BC = pose_BC[start:end]  # Get the string between the parenthesis
            pose_BC = [float(num.strip()) for num in pose_BC.split(",")]
        except (ValueError, AttributeError) as e:
            print(f"Error parsing pose_BC: {e}")
            continue

        

    

        


    if pose_BC and detections:
        pose_AC = compute_pose((x*100, y*100, pitch*100), pose_BC)
        print("A 到 C 的相對位移和朝向 (x, y, theta [deg]):")
        print(pose_AC)
    
    # 顯示影像
    cv2.imshow("AprilTag Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()