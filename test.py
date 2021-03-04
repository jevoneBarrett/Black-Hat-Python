import pyautogui

pyautogui.FAILSAFE = False

def run(x, y, num_seconds):
    pyautogui.moveTo(x, y, duration=num_seconds)
    pyautogui.moveTo(-x, -y, duration=num_seconds)

for i in range(200):
    run(5, 5, 0.7)