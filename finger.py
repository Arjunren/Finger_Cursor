import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

# Set up MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cam_w, cam_h = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

screen_w, screen_h = pyautogui.size()
frame_R = 150  # Laki ng box. Mas mataas, mas sensitive.

smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

PINCH_THRESH = 30
was_pinched = False
is_dragging = False
pinch_start_time = 0
last_click_time = 0

HOLD_DELAY = 0.3 
DOUBLE_CLICK_DELAY = 0.4 

def get_distance(p1, p2):
    """Calculate distance between two landmarks in pixels"""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def process_video():
    global plocX, plocY, clocX, clocY
    global was_pinched, is_dragging, pinch_start_time, last_click_time

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1) # Mirror image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Draw Magic Box sa screen
        cv2.rectangle(frame, (frame_R, frame_R), (cam_w - frame_R, cam_h - frame_R), (255, 0, 255), 2)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * cam_w), int(lm.y * cam_h)
                    lm_list.append((cx, cy))

                if len(lm_list) != 0:
                    x_thumb, y_thumb = lm_list[4]  # Thumb tip
                    x_index, y_index = lm_list[8]  # Index tip

                    # ==========================================
                    # 1. MOVE MOUSE (Gagana kahit naka-hold click)
                    # ==========================================
                    screen_x = np.interp(x_index, (frame_R, cam_w - frame_R), (0, screen_w))
                    screen_y = np.interp(y_index, (frame_R, cam_h - frame_R), (0, screen_h))

                    clocX = plocX + (screen_x - plocX) / smoothening
                    clocY = plocY + (screen_y - plocY) / smoothening
                    
                    try:
                        pyautogui.moveTo(clocX, clocY, _pause=False)
                        plocX, plocY = clocX, clocY
                    except pyautogui.FailSafeException:
                        pass 

                    index_dist = get_distance((x_thumb, y_thumb), (x_index, y_index))
                    is_pinched = index_dist < PINCH_THRESH
                    current_time = time.time()

                    # Kapag KAKADIKIT lang ng daliri ngayon
                    if is_pinched and not was_pinched:
                        pinch_start_time = current_time

                    # Kapag NAKADIKIT PA RIN ang daliri (Naka-hold)
                    elif is_pinched and was_pinched:
                        # Kung lumagpas na sa HOLD_DELAY ang pagkadikit at hindi pa nagda-drag
                        if not is_dragging and (current_time - pinch_start_time) > HOLD_DELAY:
                            pyautogui.mouseDown(button='left')
                            is_dragging = True
                            print("Hold Click Started! (Dragging)")

                    # Kapag BINITAWAN NA yung daliri
                    elif not is_pinched and was_pinched:
                        if is_dragging:
                            # Kung nagda-drag, i-release na ang mouse
                            pyautogui.mouseUp(button='left')
                            is_dragging = False
                            print("Hold Click Released!")
                        else:
                            # Kung binatawan agad bago mag-hold, check kung Single o Double Click
                            if current_time - last_click_time < DOUBLE_CLICK_DELAY:
                                pyautogui.click(button='right')
                                print("Double Pinch! RIGHT CLICK")
                                last_click_time = 0  # Reset
                            else:
                                pyautogui.click(button='left')
                                print("Single Pinch! LEFT CLICK")
                                last_click_time = current_time
                    
                    # Update yung previous state
                    was_pinched = is_pinched

        cv2.imshow("Hand Gesture Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print("Starting Artificial Mouse... Press 'q' to quit.")
process_video()
cap.release()
cv2.destroyAllWindows()