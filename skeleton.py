# pip install mediapipe opencv-python

import cv2
import mediapipe as mp

# Ініціалізація Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Перехоплення відео з камери ( основна камера - 0, додаткова камера - 1)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# циклічний процес обробки відео з камери
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Відобразити кадр горизонтально
    frame = cv2.flip(frame, 1)

    # Збільшити розмір кадра (наприклад, у 2 рази)
    scale_factor = 2
    frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    
    # Перетворення кадра в RGB (вимога Mediapipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Обробка кадра з використанням Mediapipe
    result = pose.process(rgb_frame)

    # Якщо знайдено опорні точки скелетона людини
    if result.pose_landmarks:
        # Візуалізувати опорні точки зеленим кольором (color=(0, 255, 0)) товщиною 7
	# Візуалізувати лінії поєднянн окремих точок червоним кольором 
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=7, circle_radius=7),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=7, circle_radius=7),
        )

        # Отримати координати опорних точок
        h, w, _ = frame.shape
        landmarks = result.pose_landmarks.landmark

        # Створення дзеркального відображення опорних точок для узгодження з лівою/правою частиною
        mirrored_landmarks = []
        for lm in landmarks:
            mirrored_landmarks.append(
                {
                    "x": 1 - lm.x,  # Координата X - відзеркалення
                    "y": lm.y,      # Координата Y залишається незмінною
                    "z": lm.z,      # Координата Z залишається незмінною
                    "visibility": lm.visibility
                }
            )

    # Показати кадр
    cv2.imshow('Mediapipe Mirror Pose', frame)

    # Вихід по клавиші 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Звільнення ресурсів
cap.release()
cv2.destroyAllWindows()
