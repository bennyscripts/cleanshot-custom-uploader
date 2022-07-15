import os
import requests
import json
import tkinter

from typing import Union

class Uploader:
    def __init__(self, window: tkinter.Tk) -> None:
        self.check_files()
        self.uploader_json = json.load(open("data/uploader.json"))
        self.http = requests.Session()
        self.window = window

        if "Headers" not in self.uploader_json:
            self.uploader_json["Headers"] = {}

        if "Arguments" not in self.uploader_json:
            self.uploader_json["Arguments"] = {}

    def check_files(self) -> None:
        for _file in os.listdir(f"data/"):
            if _file.endswith(".sxcu"):
                print(f"📁 Found SXCU uploader file.")
                os.rename(f"data/{_file}", f"data/uploader.json")
                print(f"🏷️  Renamed uploader file to uploader.json")
                break

        if not os.path.isfile(f"data/uploader.json"):
            print("❎ No uploader.json file found in data folder.")
            print("🙏 Please create a file called uploader.json in the data folder or put a ShareX config file in the data folder")
            exit(1)

    def upload_screenshot(self, screenshot_path: str) -> Union[str, None]:
        screenshot_file = screenshot_path.split("/")[-1]
        self.window.console.insert(tkinter.END, f"🔁 Uploading screenshot {screenshot_file}...")
        content_type = self.uploader_json["Body"]

        if content_type == "MultipartFormData":
            files = {self.uploader_json["FileFormName"]: open(screenshot_path, 'rb')}
            arguments = self.uploader_json["Arguments"]
            response = self.http.request(self.uploader_json["RequestMethod"], self.uploader_json["RequestURL"], files=files, data=arguments, headers=self.uploader_json["Headers"])

        if response.status_code == 200:
            content_type = response.headers["Content-Type"].split(";")[0]

            if content_type == "application/json":
                response_json = response.json()
                if "URL" in self.uploader_json:
                    uploader_url = self.uploader_json["URL"].replace("$", "")
                    json_key = uploader_url.split(":")[1]

                    if json_key in response_json:
                        return response_json[json_key]

            if content_type == "text/html":
                return response.text

        return None