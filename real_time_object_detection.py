# USAGE:
# python yolov11demo_fixed.py

import cv2
import time
import pyttsx3
from queue import Queue, Empty
import threading
from ultralytics import YOLO
import numpy as np

# ------------------- SETTINGS --------------------
CONFIDENCE_THRESHOLD = 0.5
FRAME_WIDTH = 640
ABSENCE_RESET = 1.5          # Reannounce object if gone this long (seconds)
SPEECH_QUEUE_MAX = 3         # Avoid speech stack buildup
SPEAK_INTERVAL = 2.0         # seconds between announcements
SPEECH_RATE = 170

# ----------------- TEXT TO SPEECH ----------------
engine = pyttsx3.init()
engine.setProperty('rate', SPEECH_RATE)
speech_queue = Queue()

def speech_worker():
    """Continuously speaks messages from a queue."""
    while True:
        try:
            msg = speech_queue.get(timeout=1.0)
        except Empty:
            continue
        if msg == "STOP":
            speech_queue.task_done()
            break
        try:
            engine.say(msg)
            engine.runAndWait()
        except Exception as e:
            print("[TTS ERROR]:", e)
        finally:
            speech_queue.task_done()

# Start background TTS thread
threading.Thread(target=speech_worker, daemon=True).start()

# ------------------ LOAD YOLO --------------------
print("[INFO] Loading Ultralytics YOLOv11 model...")
try:
    model = YOLO("yolo11n.pt")
    print("[INFO] Successfully loaded YOLOv11 model.")
except Exception as e:
    print(f"[WARN] YOLOv11 not found or model error: {e}")
    print("[INFO] Falling back to YOLOv8n...")
    model = YOLO("yolov8n.pt")

print("[INFO] Model loaded:", model.model_name)

# ------------------ CAMERA SETUP -----------------
print("[INFO] Starting laptop camera...")
cap = cv2.VideoCapture(0)
time.sleep(1.5)

if not cap.isOpened():
    print("[ERROR] Could not open webcam. Please check camera permissions.")
    input("Press Enter to exit...")
    exit()

print("[INFO] Camera initialized successfully.")

last_seen = {}     # Track timestamp of last detection for each object
objects_to_speak = set()
last_speak_time = time.time()

# --------------- DIRECTION FUNCTION -------------
def get_direction(cx, width):
    """Return left / center / right depending on object's horizontal position."""
    if cx < width / 3:
        return "left"
    elif cx < 2 * width / 3:
        return "center"
    else:
        return "right"

# ------------------- MAIN LOOP ------------------
try:
    cv2.namedWindow("YOLOv11 Smart Object Narrator", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("YOLOv11 Smart Object Narrator", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame not received, retrying...")
            time.sleep(0.05)
            continue

        h0, w0 = frame.shape[:2]
        if w0 != FRAME_WIDTH:
            scale = FRAME_WIDTH / float(w0)
            frame = cv2.resize(frame, (FRAME_WIDTH, int(h0 * scale)))
        h, w = frame.shape[:2]

        results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)[0]
        detections = []
        current_time = time.time()

        current_objects = set()

        for box in results.boxes:
            xyxy = box.xyxy.cpu().numpy().flatten()
            conf = float(box.conf.cpu().numpy())
            cls = int(box.cls.cpu().numpy())
            label = model.names[cls]

            x1, y1, x2, y2 = map(int, xyxy)
            cx = (x1 + x2) / 2
            direction = get_direction(cx, w)
            key = f"{label} on the {direction}"

            detections.append((x1, y1, x2, y2, label, conf, direction))
            current_objects.add(key)

            # ✅ Speak if object is new or reappeared after absence
            if key not in last_seen or (current_time - last_seen[key]) > ABSENCE_RESET:
                objects_to_speak.add(key)
                last_seen[key] = current_time
            else:
                # Still visible — update timestamp
                last_seen[key] = current_time

        # Cleanup disappeared objects
        last_seen = {k: v for k, v in last_seen.items() if current_time - v <= ABSENCE_RESET + 0.5}

        # Speak summary every SPEAK_INTERVAL seconds
        if (current_time - last_speak_time) >= SPEAK_INTERVAL:
            if objects_to_speak:
                if speech_queue.qsize() < SPEECH_QUEUE_MAX:
                    items = sorted(objects_to_speak)
                    msg = "I see: " + ", ".join(items) if len(items) > 1 else f"I see {items[0]}"
                    speech_queue.put(msg)
                    print("[SPEAK]", msg)
                    objects_to_speak.clear()
                else:
                    print("[SPEAK] queue full — postponing announcement")
            last_speak_time = current_time

        # Draw bounding boxes
        for x1, y1, x2, y2, label, conf, direction in detections:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {direction} {int(conf * 100)}%",
                        (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

        # Draw direction lines
        cv2.line(frame, (w // 3, 0), (w // 3, h), (255, 255, 255), 1)
        cv2.line(frame, (2 * w // 3, 0), (2 * w // 3, h), (255, 255, 255), 1)

        cv2.imshow("YOLOv11 Smart Object Narrator", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Exiting...")
            break

finally:
    try:
        speech_queue.put("STOP")
    except Exception:
        pass
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Camera and windows released successfully.")
