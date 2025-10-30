import os
import requests

# * 2MB = 2,048,000 bytes
# * by GitHub Copilot ✨


def setpfp(filepath: str):
    USER_ID = os.getenv("USER_ID")
    JWT_TOKEN = os.getenv("JWT_TOKEN")

    if USER_ID is None or JWT_TOKEN is None:
        raise Exception("Where .env?")

    url = f"https://api.zoom.us/v2/users/{USER_ID}/picture"

    if os.path.getsize(filepath) >= 2048000:
        raise Exception("Illegal File Size")

    picture = open(filepath, "rb")

    # * https://stackoverflow.com/questions/60287922/how-to-upload-photos-pictures-to-zoom-api-using-python-multipart-form-data-wit
    # * It works in Python but dont know why not in nodejs, So I'll stick with Python
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Accept": "application/json",
    }
    files = {
        "pic_file": picture
    }

    response = requests.post(url, files=files, headers=headers)

    if response.status_code != 201:
        print(response.json())
        raise Exception(f"Status Code is {response.status_code}")
