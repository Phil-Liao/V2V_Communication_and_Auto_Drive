import cv2
import apriltag
import socket
import threading


nickname = "test"

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 7777))

# Create an AprilTag detector
detector = apriltag.Detector()

# Open the webcam
cap = cv2.VideoCapture(1)


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

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()


while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Detect AprilTags in the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    results = detector.detect(gray)

    # Draw bounding boxes around the detected AprilTags
    for r in results:
        corners = r.corners.astype(int)
        if corners.shape[0] == 4:
            cv2.line(frame, (corners[0][0], corners[0][1]), (corners[1][0], corners[1][1]), (0, 0, 255), 2)
            cv2.line(frame, (corners[1][0], corners[1][1]), (corners[2][0], corners[2][1]), (0, 0, 255), 2)
            cv2.line(frame, (corners[2][0], corners[2][1]), (corners[3][0], corners[3][1]), (0, 0, 255), 2)
            cv2.line(frame, (corners[3][0], corners[3][1]), (corners[0][0], corners[0][1]), (0, 0, 255), 2)
            center_x = (corners[0][0] + corners[2][0]) // 2
            center_y = (corners[0][1] + corners[2][1]) // 2
            cv2.putText(frame, str(r.tag_id), (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            message = '{}: {}'.format(nickname, str(r.tag_id))
            client.send(message.encode('ascii'))
        else:
            print(f"Unexpected number of corners: {corners.shape[0]}")

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()