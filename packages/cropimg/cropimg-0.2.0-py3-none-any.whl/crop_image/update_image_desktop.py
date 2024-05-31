from crop_image.update_image import UpdateImage
import platform


class UpdateImageDesktop(UpdateImage):
    def __init__(self) -> None:
        super().__init__(self, 'Desktop')

    def update(self, path: str) -> bool:
        screenshot = self.take_screenshot()
        screenshot.save(path, format="PNG")
        return True

    def take_screenshot(self):
        system = platform.system()
        if system == "Windows":
            return self.take_screenshot_windows()
        elif system == "Darwin":
            return self.take_screenshot_mac()
        elif system == "Linux":
            return self.take_screenshot_linux()
        else:
            raise NotImplementedError(f"Unsupported OS: {system}")

    def take_screenshot_windows(self):
        import pyautogui
        screenshot = pyautogui.screenshot()
        return screenshot

    def take_screenshot_mac(self):
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        return screenshot

    def take_screenshot_linux(self):
        import pyscreenshot as ImageGrab
        screenshot = ImageGrab.grab()
        return screenshot


UpdateImageDesktop()
