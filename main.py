import cv2
import pyautogui
import numpy as np
import tkinter as tk
from tkinter import messagebox
import time


# Create a GUI window
root = tk.Tk()
root.title("Screen Recorder")

# Define the screen resolution and other parameters
resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*"XVID")
filename = "Recording.avi"
fps = 30.0
out = cv2.VideoWriter(filename, codec, fps, resolution)

# initialize variables
recording = False
paused = False

# Creates a resizable OpenCV window
cv2.namedWindow('Recording:)', cv2.WINDOW_NORMAL)


def start_recording():
    global recording, paused
    recording = True
    frame_time = 1.0 / fps
    while recording:
        start_time = time.time()
        if not paused:
            img = pyautogui.screenshot()
            frame = np.array(img)
            out.write(frame)
            cv2.imshow('Recording:)', frame)

        key = cv2.waitKey(1)
        if key == ord('a'):
            recording = False
            replay_or_save()
        elif key == ord('p'):
            paused = True
        elif key == ord('r'):
            paused = False
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time < frame_time:
            time.sleep(frame_time - elapsed_time)

    out.release()
    cv2.destroyAllWindows()

# Define the replay function


def replay_recording():
    replay = True
    while replay:
        cap = cv2.VideoCapture(filename)

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Recording:)', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

        replay = messagebox.askyesno("Replay Recording", "Do you want to replay the recording?")


def save_recording():
    try:
        save = messagebox.askyesno("Save Recording", "Do you want to save the recording to a file?")
        if not save:
            import os
            os.remove(filename)
    except OSError as e:
        if 'No space left on device' in str(e):
            print("There is not enough space left on device")
        else:
            raise


def replay_or_save():
    replay_recording()
    save_recording()


start_button = tk.Button(root, text="Start Recording", command=start_recording)

# Add the buttons to the GUI
start_button.pack()

# Run the GUI
root.mainloop()
