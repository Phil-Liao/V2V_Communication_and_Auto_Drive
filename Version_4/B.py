import cv2
import numpy as np
import math
import pyapriltags as apriltag
import socket
import threading

nickname = 'B' #Name of the Car

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.50.40', 8888))

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
                print(message)
        except:
            # Close Connection When Error
            client.close()
            print("[DISCONNECTED] An error occured.")
            break

# Sending Messages To Server
def write_to_server(data:str):
    message = '{}: {}'.format(nickname, data)
    client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()




# 設定相機內參 (根據相機校正調整)
camera_matrix = np.array([[797.19922282, 0, 319.75614916],  # fx
                          [0, 801.8848903, 259.20202143],  # fy
                          [0, 0, 1]])     # cx, cy
dist_coeffs = np.array([[3.74005891e-02, -1.96034587e+00 ,-2.19501972e-03  ,2.93313263e-03
   ,2.10149607e+01]]) # 假設無畸變，若有請填入相機校正值

# 設定 AprilTag 大小 (單位：公尺)
tag_size = 0.1016  # 10cm

# 初始化 AprilTag 偵測器
detector = apriltag.Detector(families='tag36h11')

# 開啟攝影機
cap = cv2.VideoCapture(1)  # 0 代表預設攝影機

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
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

        write_to_server(str((round(x*100, 1), round(y*100, 1), round(pitch, 1))))
        

    # 顯示影像
    cv2.imshow("AprilTag Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

