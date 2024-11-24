# TO USE THIS SCRIPT: $ conda activate mediapipe_env

import cv2
import mediapipe as mp
import time
from threading import Thread
import queue

class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        
        # Try to set higher resolution
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Try to set higher FPS
        self.stream.set(cv2.CAP_PROP_FPS, 60)
        
        # Set buffer size to minimum
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.queue = queue.Queue(maxsize=2)
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            if not self.queue.full():
                ret, frame = self.stream.read()
                if ret:
                    if not self.queue.empty():
                        try:
                            self.queue.get_nowait()
                        except queue.Empty:
                            pass
                    self.queue.put(frame)

    def read(self):
        return self.queue.get()

    def stop(self):
        self.stopped = True
        self.stream.release()

def find_droidcam():
    """Try different camera indices to find DroidCam"""
    for index in range(10):
        print(f"Trying camera index {index}...")
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Get and print camera properties
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                print(f"Found camera at index {index}")
                print(f"Default resolution: {width}x{height}")
                print(f"Default FPS: {fps}")
                cap.release()
                return index
            cap.release()
    return -1

print("Looking for DroidCam...")
camera_index = find_droidcam()

if camera_index == -1:
    print("Could not find any working camera")
    exit()

# Initialize the video stream thread
print("Starting video stream thread...")
vs = VideoStream(camera_index).start()
time.sleep(1.0)  # Allow camera to warm up

# Initialize MediaPipe hands with performance optimization
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Performance optimization settings for MediaPipe
with mp_hands.Hands(
    static_image_mode=False,  # Set to False for faster processing
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5  # Lowered for better performance
) as hands:
    
    print("Starting main loop...")
    frame_count = 0
    start_time = time.time()
    fps_start_time = start_time
    fps_counter = 0
    
    while True:
        try:
            frame = vs.read()
            
            # FPS calculation
            fps_counter += 1
            if (time.time() - fps_start_time) > 1.0:
                fps = fps_counter / (time.time() - fps_start_time)
                fps_counter = 0
                fps_start_time = time.time()
                print(f"Current FPS: {fps:.2f}")

            # Process image with performance optimizations
            # Convert to RGB without copying
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)

            # Process frame
            image.flags.writeable = False  # Performance optimization
            results = hands.process(image)
            image.flags.writeable = True

            # Convert back to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw hand landmarks if detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                    )

            # Add FPS display
            cv2.putText(image, f'FPS: {int(fps)}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show the frame
            cv2.imshow('Hand Recognition (Optimized)', image)

        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            continue

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
vs.stop()
cv2.destroyAllWindows()