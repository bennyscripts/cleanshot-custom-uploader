import os
import pyperclip
import asyncio

from utils import notifier
from utils import uploader
from utils import files

async def main():
    SCREENSHOT_DIR_PATH = f"{os.path.expanduser('~')}/Pictures"
    UPLOADER = uploader.Uploader()

    if not os.path.exists(os.path.join(SCREENSHOT_DIR_PATH, "Screenshots")):
        os.makedirs(os.path.join(SCREENSHOT_DIR_PATH, "Screenshots"))
        print("Make sure to set your Cleanshot export directory to: " + SCREENSHOT_DIR_PATH)

    notifier.send("File Uploader", "Uploader started in the background.")
    print("✅ Uploader started in the background.")

    screenshot_dir = os.path.join(SCREENSHOT_DIR_PATH, "Screenshots")
    stored_files = os.listdir(screenshot_dir)

    while True:
        newest_file = await files.get_newest_file(screenshot_dir)
        newest_file_no_path = newest_file.split("/")[-1]

        if newest_file_no_path not in stored_files:
            url = await UPLOADER.upload_screenshot(newest_file)
            pyperclip.copy(url)
            stored_files.append(newest_file_no_path)

            print(f"✅ Copied to clipboard: {url}")
            notifier.send("File Uploader", "Screenshot copied to clipboard")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())