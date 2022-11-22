import pyautogui
import time

def start():
    flagStart = False
    while flagStart == False:
        flagStart = input("Press S (or s) to start, Ctrl+C to abort: ") in ["s", "S"]
    
    screen = pyautogui.size()
    
    print(screen)
    
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    time.sleep(.2)
    pyautogui.keyUp('alt')
    pyautogui.moveTo(screen[0]/2, screen[1]/2, 0.5)
    pyautogui.click(button='right')
    pyautogui.move(5, 5)
    pyautogui.click(button='left') 
    pyautogui.press('enter')
    pyautogui.move(600/1920*screen[0], -390/1080*screen[1])
    pyautogui.click(button='left') 
    pyautogui.click(button='left') 
    pyautogui.moveTo(screen[0]/2, screen[1]/2, 0.5)


if __name__ == '__main__':
    start()
