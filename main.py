import threading
from helper import MouseAndScreenshotHelper
import PIL
import numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import matplotlib.animation as animation
from dotenv import load_dotenv
import os

load_dotenv()

SCREENSHOT_X = int(os.getenv('SCREENSHOT_X'))
SCREENSHOT_Y = int(os.getenv('SCREENSHOT_Y'))
SCREENSHOT_WIDTH = int(os.getenv('SCREENSHOT_WIDTH'))
SCREENSHOT_HEIGHT = int(os.getenv('SCREENSHOT_HEIGHT'))
CLICK_X = int(os.getenv('CLICK_X'))
CLICK_Y = int(os.getenv('CLICK_Y'))
THRESHOLD = float(os.getenv('THRESHOLD')) / 100

animation.Animation.cache_frame_data = False
helper = MouseAndScreenshotHelper()
need_update = True

def get_screen_image():
    helper.screenshot_at_position(
        x=SCREENSHOT_X,
        y=SCREENSHOT_Y,
        width=SCREENSHOT_WIDTH,
        height=SCREENSHOT_HEIGHT,
        output_path="./screenshots/screenshot.png"
    )
    return numpy.array(PIL.Image.open("./screenshots/screenshot.png"))


def jump_to(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    helper.click_at_position(x=CLICK_X, y=CLICK_Y)
    time.sleep(0.2)
    print("clicking")
    helper.click_at_position(x=CLICK_X, y=CLICK_Y, hold_time=distance * THRESHOLD)
    print("clicked")
    helper.command_tab()
    time.sleep(0.2)


prev_x = 0


def on_click(event, coor=[]):
    global need_update, prev_x
    if (event.xdata != prev_x):
        coor.append((event.xdata, event.ydata))
        prev_x = event.xdata
    else:
        return
    
    print("coor length: ", len(coor))
    if len(coor) == 2:
        jump_to(coor[0], coor[1])
        coor.clear()

    need_update = True


def update_screen(frame):
    global need_update
    if need_update:
        time.sleep(1)
        axes_image.set_array(get_screen_image())
        need_update = False
    return axes_image,


if __name__ == "__main__":
    figure = plt.figure()
    axes_image = plt.imshow(get_screen_image(), animated=True)
    figure.canvas.mpl_connect('button_press_event', on_click)
    ani = FuncAnimation(figure, update_screen, interval=50, blit=True, cache_frame_data=False)
    plt.show()