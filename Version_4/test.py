import cv2
import time

cap = cv2.VideoCapture(1)  # or your video file path

fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Reported FPS: {fps}")

# Initialize variables for FPS calculation
prev_time = 0
frame_count = 0
fps_sum = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time

    # Update FPS statistics
    fps_sum += fps
    frame_count += 1

    # Display FPS on the frame
    fps_text = f"FPS: {fps:.2f}"
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Calculate and print average FPS
if frame_count > 0:
    avg_fps = fps_sum / frame_count
    print(f"Average FPS: {avg_fps:.2f}")