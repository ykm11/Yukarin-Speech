#coding:utf-8

import win32gui
import win32con
import time
import subprocess

app_name = "C:/Program Files (x86)/AHS/VOICEROID+/YukariEX/VOICEROID.exe"

def isVoiceRoidRunning(): # Check running exec/process by means of tasklist cmd
    procs = subprocess.Popen(
        "tasklist",
        stdout=subprocess.PIPE,
        shell=True,
    ).communicate()[0].split(b"\n")
    for proc in procs:
        proc = proc.rstrip()
        if b"VOICEROID" in proc:
            print("Already started")
            return True
    return False

class VoiceRoidErr(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return str(self.reason)

class VoiceRoid(object):
    def __init__(self, name):
        self.name = name
        self.parentHwnd = win32gui.FindWindow(None, name)

        if self.parentHwnd == 0:
            raise VoiceRoidErr("VoiceRoidNotFound")
        self.play = self.getHandle(text="再生")[0]
        self.textbox = self.getHandle(name="WindowsForms10.RichEdit20W")[0]

    def getHandle(self, **args):
        result = []

        def enumCallback(hwnd, args):
            if args.get("text"):
                if args["text"] in win32gui.GetWindowText(hwnd):
                    result.append(hwnd)
            elif args.get("name"):
                if args["name"] in win32gui.GetClassName(hwnd):
                    result.append(hwnd)

        win32gui.EnumChildWindows(
            self.parentHwnd,
            enumCallback,
            args
        )
        return result

    def sendText(self, hwnd, text):
        win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)

    def say(self, text):
        while True: # waiting until playing stops
            time.sleep(0.15)
            if len(self.getHandle(text="一時停止")) < 1:
                break
        self.sendText(self.textbox, text)

        win32gui.SendMessage(self.play, win32con.BM_CLICK, 0, 0)

if __name__ == "__main__":
    import sys
    args = sys.argv
    print(args)

    if not isVoiceRoidRunning(): # otherwise, start up VOICEROID by Popen
        p = subprocess.Popen(app_name)
        time.sleep(6)

    if 1 < len(args):
        voiceroid = VoiceRoid("VOICEROID＋ 結月ゆかり EX")
        text = " ".join(args[1:]) ## $python yukari.py TEXT1 TEXT2, ...
        voiceroid.say(text)