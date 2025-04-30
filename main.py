import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import math

# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.pos = (x, y)
        self.size = (w, h)
        self.text = text

    def draw(self, img, is_active=False):
        x, y = self.pos
        w, h = self.size

        overlay = img.copy()

        # Default grey transparent fill
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (100, 100, 100), cv2.FILLED)

        # If pressed, draw green on top
        if is_active:
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)

        # Blend overlay
        alpha = 0.4 if not is_active else 0.3
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Text
        font_scale = 1.2 if len(self.text) == 1 else 0.8
        text_offset = 30 if len(self.text) == 1 else 20
        cv2.putText(img, self.text, (x + 10, y + text_offset), cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), 2)

    def is_pressed(self, x, y):
        bx, by = self.pos
        bw, bh = self.size
        return bx < x < bx + bw and by < y < by + bh

# Keyboard layout
keyboard_keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Bksp"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "?"],
    ["Space"]
]

# Configs
key_width, key_height = 60, 60
space_width = key_width * 6
start_y = 100
gap = 10

# Calculate center alignment
def create_keyboard():
    buttons = []
    for i, row in enumerate(keyboard_keys):
        total_row_width = sum(space_width if key == "Space" else key_width for key in row) + gap * (len(row) - 1)
        start_x = (1280 - total_row_width) // 2
        x = start_x
        y = start_y + i * (key_height + gap)
        for key in row:
            w = space_width if key == "Space" else key_width
            buttons.append(Button(x, y, w, key_height, key))
            x += w + gap
    return buttons

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

buttons = create_keyboard()
final_text = ""
delay_counter = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detect hands
    hands, img = detector.findHands(img, draw=False)

    # Get hand landmarks
    x1, y1 = 0, 0
    active_button = None

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        x1, y1 = lmList[8][0], lmList[8][1]  # Index tip
        x2, y2 = lmList[4][0], lmList[4][1]  # Thumb tip

        # Draw green dot as pointer
        cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

        # Draw red dot as thumb tip
        cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)

        # Pinch detection (distance between index and thumb)
        distance = math.hypot(x2 - x1, y2 - y1)

        # Draw Red line if pinch not detected
        if distance > 40:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        else:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        if distance < 40 and delay_counter == 0:
            for button in buttons:
                if button.is_pressed(x1, y1):
                    text = button.text
                    if text == "Bksp":
                        final_text = final_text[:-1]
                        pyautogui.press('backspace')
                    elif text == "Enter":
                        final_text += '\n'
                        pyautogui.press('enter')
                    elif text == "Space":
                        final_text += ' '
                        pyautogui.press('space')
                    else:
                        final_text += text
                        pyautogui.write(text)
                    delay_counter = 1
                    break

        active_button = next((b for b in buttons if b.is_pressed(x1, y1)), None)

    # Draw buttons
    for button in buttons:
        button.draw(img, is_active=(button == active_button))

    # Text box
    cv2.rectangle(img, (100, 550), (1180, 650), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, final_text[-60:], (110, 620), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    # Delay counter for debounce
    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()