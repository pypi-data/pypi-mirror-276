from crop_image.update_image import UpdateImage
import adb_tool_py as adb_tool
import adb_tool_py.command as command


class UpdateImageAdb(UpdateImage):
    def __init__(self, name: str) -> None:
        super().__init__(self, name)

    def update(self, path:str) -> bool:
        adb = adb_tool.AdbTool(serial=self.get_name())
        adb.capture_screenshot()
        adb.save_screenshot(path)
        return True

result = command.command('adb', 'devices')
lines = result.stdout.splitlines()
devices = [line for line in lines if line.strip() and not line.startswith('List of devices attached')]
for device in devices:
    UpdateImageAdb(device.split()[0])
