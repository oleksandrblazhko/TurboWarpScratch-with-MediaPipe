# pip install mediapipe opencv-python websockets

import cv2
import mediapipe as mp
import asyncio
import websockets
import json

mp_pose = mp.solutions.pose

NAMES = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index"
]

NAME_TO_INDEX = {
    "nose": 0,
    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,
    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,
    "left_ear": 7,
    "right_ear": 8,
    "mouth_left": 9,
    "mouth_right": 10,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_pinky": 17,
    "right_pinky": 18,
    "left_index": 19,
    "right_index": 20,
    "left_thumb": 21,
    "right_thumb": 22,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32
}

async def send_pose(websocket):
    # вибір зовнішньої камери - 1, вбудованої - 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    with mp_pose.Pose() as pose:
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Камера не доступна")
                    break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    
                    skeletons = {}
                    for name in NAMES:
                        index = NAME_TO_INDEX[name]
                        skeletons[f"{name}_x"] = landmarks[index].x
                        skeletons[f"{name}_y"] = landmarks[index].y
                        skeletons[f"{name}_z"] = landmarks[index].z
                    
                    await websocket.send(json.dumps(skeletons))

                # затримка оновлення даних в секундах
                await asyncio.sleep(0.05)

        except websockets.exceptions.ConnectionClosed:
            print("Клієнт відключився")
        finally:
            cap.release()

async def main():
    async with websockets.serve(send_pose, "localhost", 8765):
        print("WebSocket сервер запущено на ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
