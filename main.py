import time
import threading
import cv2
import mss
import numpy as np
import win32gui
import win32con
import pyautogui
from pynput.keyboard import Controller

def get_window(hwnd_name):
    hwnd = win32gui.FindWindow(None, hwnd_name)
    if hwnd == 0:
        raise Exception(f"Window not found: {hwnd_name}")
    win32gui.SetForegroundWindow(hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    return hwnd, rect

def click_and_press(rect, keys_sequence, default_delay=0.2):
    time.sleep(0.5)  # Let the capture thread start
    x = rect[0] + (rect[2] - rect[0]) // 2
    y = rect[1] + (rect[3] - rect[1]) // 2
    pyautogui.click(x, y)
    time.sleep(0.3)
    kb = Controller()

    for action in keys_sequence:
        if isinstance(action, dict):
            keys = action.get('keys')
            delay = action.get('delay', default_delay)
        else:
            keys = action
            delay = default_delay

        if isinstance(keys, (list, tuple)):  # simultaneous press
            for key in keys:
                kb.press(key)
            time.sleep(delay)
            for key in keys:
                kb.release(key)
        else:  # single key
            kb.press(keys)
            time.sleep(delay)
            kb.release(keys)        

def compress_image(img, quality=50):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', img, encode_param)
    return cv2.imdecode(encimg, 1) if result else img

def capture_window(rect, scale=0.5):
    bbox = {"top": rect[1], "left": rect[0], "width": rect[2] - rect[0], "height": rect[3] - rect[1]}
    template_purple = cv2.imread('images/wizzard_purple_resized.png')
    template_yellow = cv2.imread('images/wizzard_yellow_resized.png')
    if template_purple is None or template_yellow is None:
        raise FileNotFoundError("Template images not found.")

    template_purple = cv2.resize(template_purple, (0, 0), fx=scale, fy=scale)
    template_yellow = cv2.resize(template_yellow, (0, 0), fx=scale, fy=scale)
    h_purple, w_purple = template_purple.shape[:2]
    h_yellow, w_yellow = template_yellow.shape[:2]
    confidence = 0.6

    with mss.mss() as sct:
        while True:
            img = np.array(sct.grab(bbox))[:, :, :3]
            resized = cv2.resize(img, (0, 0), fx=scale, fy=scale)
            compressed = compress_image(resized, quality=40)

            res_purple = cv2.matchTemplate(compressed, template_purple, cv2.TM_CCOEFF_NORMED)
            for pt in zip(*np.where(res_purple >= confidence)[::-1]):
                cv2.rectangle(compressed, pt, (pt[0]+w_purple, pt[1]+h_purple), (255, 0, 255), 2)
                # print(f"Purple at x: {pt[0]}, y: {pt[1]}")

            res_yellow = cv2.matchTemplate(compressed, template_yellow, cv2.TM_CCOEFF_NORMED)
            for pt in zip(*np.where(res_yellow >= confidence)[::-1]):
                cv2.rectangle(compressed, pt, (pt[0]+w_yellow, pt[1]+h_yellow), (0, 255, 255), 2)
                # print(f"Yellow at x: {pt[0]}, y: {pt[1]}")

            cv2.imshow("Game Capture", compressed)
            if cv2.waitKey(1) == 27:  # ESC
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    keys_yellow = [
        {'keys': 'd', 'delay': 0.6},
        {'keys': ('d', 'w'), 'delay': 0.5},
        {'keys': 'd', 'delay': 0.2},
        {'keys': 'a', 'delay': 0.5},
        's',
        {'keys': ('a', 'w'), 'delay': 0.5},
        {'keys': 'a', 'delay': 0.5},
        {'keys': ('d', 'w'), 'delay': 0.5},
        {'keys': ('d', 'w'), 'delay': 0.5},
        {'keys': ('d', 'w'), 'delay': 0.5},
        {'keys': ('d', 'w'), 'delay': 0.5},

    ]
    keys_purple = [
        {'keys': 'j', 'delay': 0.6},
        {'keys': ('j', 'i'), 'delay': 0.5},
        {'keys': 'j', 'delay': 0.2},
        {'keys': 'l', 'delay': 0.5},
        's',
        {'keys': ('i', 'l'), 'delay': 0.5},
        {'keys': 'l', 'delay': 0.5},
        {'keys': ('i', 'j'), 'delay': 0.5},
        {'keys': ('i', 'j'), 'delay': 0.5},
        {'keys': ('i', 'j'), 'delay': 0.5},
        {'keys': ('i', 'j'), 'delay': 0.5},
    ]

    hwnd, rect = get_window("Ambidextro")

    thread_click_purple = threading.Thread(target=click_and_press, args=(rect, keys_purple))
    thread_click_yellow = threading.Thread(target=click_and_press, args=(rect, keys_yellow))
    thread_capture = threading.Thread(target=capture_window, args=(rect,))

    thread_capture.start()
    thread_click_yellow.start()
    thread_click_purple.start()

    # Wait for capture to finish (when ESC is pressed)
    thread_capture.join()
