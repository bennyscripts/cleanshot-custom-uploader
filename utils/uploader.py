import os
import requests
import json

for _file in os.listdir(f"data/"):
    if _file.endswith(".sxcu"):
        os.rename(f"data/{_file}", f"data/uploader.json")
        break

if not os.path.isfile(f"data/uploader.json"):
    print("No uploader.json file found in data folder.")
    print("Please create a file called uploader.json in the data folder or put a ShareX config file in the data folder")
    exit(1)

UPLOADER_JSON = json.load(open("data/uploader.json"))

def upload_screenshot(screenshot_path):
    print("Uploading screenshot...") 
    content_type = UPLOADER_JSON["Body"]

    if content_type == "MultipartFormData":
        files = {UPLOADER_JSON["FileFormName"]: open(screenshot_path, 'rb')}
        arguments = UPLOADER_JSON["Arguments"]
        response = requests.request(UPLOADER_JSON["RequestMethod"], UPLOADER_JSON["RequestURL"], files=files, data=arguments, headers=UPLOADER_JSON["Headers"])
        
    if response.status_code == 200:
        url = response.text
        return url

    return None