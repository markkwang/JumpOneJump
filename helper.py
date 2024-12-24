from pynput.mouse import Controller, Button
import pyautogui
import time

class MouseAndScreenshotHelper:
    def __init__(self):
        self.mouse = Controller()

    def click_at_position(self, x, y, hold_time=0.2, delay_before=0.1, delay_after=0.1):
        time.sleep(delay_before)
        self.mouse.position = (x, y)
        self.mouse.press(Button.left)
        time.sleep(hold_time)
        self.mouse.release(Button.left)
        time.sleep(delay_after)

    def screenshot_at_position(self, x, y, width, height, output_path="screenshot.png"):
        region = (x, y, width, height)
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(output_path)

    def command_tab(self, delay_before=0.1, delay_after=0.1):
        """
        Simulates pressing Command + Tab on macOS to switch applications.
        """
        time.sleep(delay_before)
        pyautogui.keyDown('command')
        pyautogui.press('tab')
        pyautogui.keyUp('command')
        time.sleep(delay_after)

if __name__ == "__main__":
    helper = MouseAndScreenshotHelper()
    helper.click_at_position(x=500, y=300, hold_time=0.2)
    helper.screenshot_at_position(x=500, y=300, width=100, height=100, output_path="example_screenshot.png")
    helper.command_tab()