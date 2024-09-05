# pyinstaller --onefile --uac-admin --icon=assets/logo.ico XooX.py

import os
import time
import shutil
import base64
import requests
import pyautogui
from time import mktime
import DiscordRichPresence
from datetime import datetime
from dotenv import load_dotenv


def RunDiscordRPC(
    details,
    state,
    large_text,
    small_text,
    large_image,
    small_image,
    buttons_label1,
    buttons_url1,
    buttons_label2,
    buttons_url2,
):
    DiscordRichPresenceActivity.set_activity(
        {
            "state": state,
            "details": details,
            "timestamps": {"start": start_time},
            "assets": {
                "small_text": small_text,
                "small_image": small_image,
                "large_text": large_text,
                "large_image": large_image,
            },
            "buttons": [
                {"label": buttons_label1, "url": buttons_url1},
                {"label": buttons_label2, "url": buttons_url2},
            ],
        }
    )
    time.sleep(1)


def DiscordSend(content,Username,avatar_url):
    with open(asset + "\\" + str(content) + ".png", "rb") as file:
        file_data = file.read()
    files = {"file": (asset + "\\" + str(content) + ".png", file_data, "image/png")}
    response = requests.post(
        webhook_url,
        files=files,
        data={
            "username": Username,
            "content": "||Username: "
            + Username
            + "\n"
            + "Year: "
            + year
            + "\n"
            + "H_M_S: "
            + H_M_S
            + "\n"
            + "Index: "
            + str(content)
            + "||",
            "avatar_url":avatar_url,
        },
    )


if __name__ == "__main__":
    # Load the .env file
    load_dotenv()
    start_time = mktime(time.localtime())
    APPLICATION_ID = os.getenv("APPLICATION_ID")
    try:
        print("Discord Rich Presence connection successful.")
        DiscordRichPresenceActivity = DiscordRichPresence.DiscordIpcClient.for_platform(
            APPLICATION_ID
        )
        time.sleep(1)
    except:
        print("Failed to set Discord Rich Presence activity, trying again in 5 seconds")
        time.sleep(5)
    DISCORD_INVIRE = os.getenv("buttons_url1")
    DISCORD_SUPPORT_INVIRE = os.getenv("buttons_url2")
    INDEX = 0
    RunDiscordRPC(
        details=os.getenv("details"),
        state=os.getenv("state"),
        large_text=os.getenv("large_text"),
        small_text=os.getenv("small_text"),
        large_image=os.getenv("large_image"),
        small_image=os.getenv("small_image"),
    )

    cuttenttime = datetime.now()
    PER_FRAMES = int(os.getenv("PER_FRAMES"))

    year = str(str(cuttenttime.today()).split()[0].split("-")[0])
    H_M_S = str(cuttenttime.strftime("%H:%M:%S").replace(":", "-"))
    cuttenttime = year + "-" + H_M_S
    main_folder_path = os.path.abspath(os.getcwd())
    asset = main_folder_path + "\\" + str(cuttenttime)
    if os.path.exists(asset):
        shutil.rmtree(asset)
        os.mkdir(asset)
    else:
        os.mkdir(asset)
    if os.getenv("IS_LOCAL") in "false":
        webhook_url = input("Discord Text Channel WebHook URL: ")
        Username = os.getenv("PER_FRAMES")
        while True:
            INDEX += 1
            if INDEX % PER_FRAMES == 0:
                screenshot = pyautogui.screenshot()
                screenshot.save(asset + "\\" + str(INDEX) + ".png")
                DiscordSend(INDEX,Username,os.getenv("avatar_url"))
                try:
                    if INDEX != 0:
                        if os.path.exists(asset + "\\" + str(INDEX - 1) + ".png"):
                            os.remove(asset + "\\" + str(INDEX - 1) + ".png")
                except:
                    pass

    elif os.getenv("IS_LOCAL") in "true":
        while True:
            INDEX += 1
            if INDEX % PER_FRAMES == 0:
                screenshot = pyautogui.screenshot()
                screenshot.save(asset + "\\" + str(INDEX) + ".png")
    else:
        pass
