import os
import pyperclip
import tkinter

from utils import notifier
from utils import uploader
from utils import files

class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screenshot Uploader")
        self.geometry("450x250")
        self.resizable(False, False)

        self.create_widgets()
        self.create_loops()
        self.setup()

    def create_widgets(self):
        self.console = tkinter.Listbox(self, width=450, height=250)
        self.console.pack()

    def create_loops(self):
        self.after(1, self.check_screenshots)

    def setup(self):
        self.screenshot_dir_path = f"{os.path.expanduser('~')}/Pictures"
        self.uploader = uploader.Uploader(self)

        if not os.path.exists(os.path.join(self.screenshot_dir_path, "Screenshots")):
            os.makedirs(os.path.join(self.screenshot_dir_path, "Screenshots"))
            self.console.insert(tkinter.END, "ℹ️ Make sure to set your Cleanshot export directory to: " + self.screenshot_dir_path)

        notifier.send("Screenshot Uploader", "Uploader started in the background.")
        self.console.insert(tkinter.END, "🏞 Screenshot Uploader has started!")
        self.console.insert(tkinter.END, "\tℹ️ Take a screenshot and save it to pictures/screenshots and it will be uploaded to the image host set in data/uploader.json.")
        self.console.insert(tkinter.END, "\tℹ️ If you need to edit any settings, open data/uploader.json and edit the values.")
        self.console.insert(tkinter.END, "")

        self.screenshot_dir = os.path.join(self.screenshot_dir_path, "Screenshots")
        self.stored_files = os.listdir(self.screenshot_dir)

    def check_screenshots(self):
        newest_file = files.get_newest_file(self.screenshot_dir)
        newest_file_no_path = newest_file.split("/")[-1]

        if newest_file_no_path not in self.stored_files:
            url = self.uploader.upload_screenshot(newest_file)
            pyperclip.copy(url)
            self.stored_files.append(newest_file_no_path)

            self.console.insert(tkinter.END, f"\t✅ Copied to clipboard: {url}")
            self.console.insert(tkinter.END, "")
            notifier.send("Screenshot Uploader", "Screenshot copied to clipboard")

        self.after(1, self.check_screenshots)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    Window().run()