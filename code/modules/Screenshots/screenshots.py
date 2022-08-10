
import pyautogui
import os
from datetime import date

directory        = "../files/ss"
limit            = 5

screenshot_limit = {
    "limit" : limit,
    "message" : f'Se alcanzó el límite de {limit} Captura{"s" if limit != 0 else ""}'       
}

limitData       = lambda key: screenshot_limit[key]
screenshotLimit = lambda: len(os.listdir(directory)) >= screenshot_limit["limit"]
screenshotList  = lambda separator = ">": f"{separator} " + '\n- '.join(os.listdir(directory))

def screenshot(): 
    my_screenshot = pyautogui.screenshot()
    if len(os.listdir(directory)) > 0:
        last_ss       = os.listdir(directory)[-1]
        last_ss       = last_ss.split()
        new_ss_index  = int(last_ss[0].replace("[", "").replace("]", "")) + 1
    else: new_ss_index = 1

    file_name     = f"[{new_ss_index}] {date.today()}.jpg"
    file_path     = f"{directory}/{file_name}"
    my_screenshot.save(file_path)
    return file_path

def showScreenshot(name): pass

def test():
    print(os.listdir(directory)[-1])



