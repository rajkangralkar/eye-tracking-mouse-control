import cv2
import mediapipe as mp
import pyautogui
import time

# CONFIG
MOBILE_CAM_URL = 'your mobile ipv4'
MOVE_STEP = 50
CENTER_TOLERANCE = 20
DOUBLE_BLINK_INTERVAL = 0.4

# Setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

cap = cv2.VideoCapture(MOBILE_CAM_URL)
screen_width, screen_height = pyautogui.size()
prev_blink_time = 0
blink_count = 0

def is_blinking(landmarks, upper_idx, lower_idx, h):
    upper = landmarks[upper_idx]
    lower = landmarks[lower_idx]
    return abs((upper.y - lower.y) * h) < 5

def get_movement_direction(iris_x, iris_y, center_x, center_y):
    dx = iris_x - center_x
    dy = (iris_y - center_y) * 1.8  # Increase vertical sensitivity

    if abs(dx) < CENTER_TOLERANCE and abs(dy) < CENTER_TOLERANCE * 0.6:
        return "center"
    elif abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    else:
        return "down" if dy > 0 else "up"


while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Cannot access IP webcam")
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        try:
            # Eye centers
            left_eye_center_x = (landmarks[33].x + landmarks[133].x) / 2 * w
            left_eye_center_y = (landmarks[159].y + landmarks[145].y) / 2 * h
            right_eye_center_x = (landmarks[362].x + landmarks[263].x) / 2 * w
            right_eye_center_y = (landmarks[386].y + landmarks[374].y) / 2 * h
            avg_eye_center_x = (left_eye_center_x + right_eye_center_x) / 2
            avg_eye_center_y = (left_eye_center_y + right_eye_center_y) / 2

            # Iris positions
            left_iris_x = landmarks[468].x * w
            left_iris_y = landmarks[468].y * h
            right_iris_x = landmarks[473].x * w
            right_iris_y = landmarks[473].y * h
            avg_iris_x = (left_iris_x + right_iris_x) / 2
            avg_iris_y = (left_iris_y + right_iris_y) / 2

            # Movement
            direction = get_movement_direction(avg_iris_x, avg_iris_y,
                                               avg_eye_center_x, avg_eye_center_y)

            if direction == "left":
                pyautogui.moveRel(-MOVE_STEP, 0)
            elif direction == "right":
                pyautogui.moveRel(MOVE_STEP, 0)
            elif direction == "up":
                pyautogui.moveRel(0, -MOVE_STEP)
            elif direction == "down":
                pyautogui.moveRel(0, MOVE_STEP)

            # Blink detection using one eye (left)
            if is_blinking(landmarks, 159, 145, h):
                now = time.time()
                if now - prev_blink_time < DOUBLE_BLINK_INTERVAL:
                    blink_count += 1
                else:
                    blink_count = 1
                prev_blink_time = now

                if blink_count == 2:
                    pyautogui.doubleClick()
                    print("🖱️ Double Click")
                    blink_count = 0
                elif blink_count == 1:
                    pyautogui.click()
                    print("🖱️ Single Click")

                time.sleep(0.3)

            # Visuals
            cv2.circle(frame, (int(avg_iris_x), int(avg_iris_y)), 5, (0, 255, 0), -1)
            cv2.circle(frame, (int(avg_eye_center_x), int(avg_eye_center_y)), 5, (0, 0, 255), 2)
            cv2.putText(frame, f"Direction: {direction}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        except IndexError:
            print("⚠️ Landmark detection incomplete")

    else:
        cv2.putText(frame, "Face Not Detected", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Eye-Controlled Mouse (Both Eyes)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
