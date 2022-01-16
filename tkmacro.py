import tkinter as tk
import pyautogui
import time
import ctypes

import re


iniPx = 0
iniPy = 0
onExec = False
testMode = False


def isPressing(key):
    ks = ctypes.windll.user32.GetAsyncKeyState(key)
    return bool(ks & 0x8000)

def isEscPressing():
    return isPressing(0x1B)

def click(x, y, keepPos):
    if keepPos:
        p = pyautogui.position()
        pyautogui.click(x=x, y=y, clicks=1, interval=0, button="left")
        pyautogui.moveTo(p.x, p.y)
    else:
        pyautogui.click(x=x, y=y, clicks=1, interval=0, button="left")

def move(x, y):
    pyautogui.moveTo(x, y)

def parseLocation(arg):
    rr2 = re.match('([0-9]+) +([0-9]+)', arg)
    px = int(rr2.group(1))
    py = int(rr2.group(2))
    return px, py

def execParamCmd(cmd, arg):
    if cmd == 'Click':
        px, py = parseLocation(arg)
        click(px, py, True)
    elif cmd == 'Move':
        px, py = parseLocation(arg)
        move(px, py)
    elif cmd == 'Wait':
        wt = float(arg)
        time.sleep(wt * 0.001)
    elif cmd == 'Copy':
        pyautogui.hotkey("ctrl", "c")
    elif cmd == 'Paste':
        pyautogui.hotkey("ctrl", "v")
    elif cmd == 'SelAll':
        pyautogui.hotkey("ctrl", "a")
    elif cmd == 'ResetPos':
        pyautogui.moveTo(iniPx, iniPy)

def execCmd(l):
    rr = re.match('([a-zA-Z]+) +(.+)', l)
    if not rr is None:
        cmd = rr.group(1)
        arg = rr.group(2)
        execParamCmd(cmd, arg)
    elif l != '':
        cmd = l
        execParamCmd(cmd, None)

def exec():
    global onExec
    global iniPx
    global iniPy

    if onExec:
        return

    onExec = True

    p = pyautogui.position()
    iniPx = p.x
    iniPy = p.y
    t = txt.get( "1.0", "end")
    v = t.splitlines()
    for l in v:
        if isEscPressing():
            break
        execCmd(l)

    onExec = False

def foc():
    buttonFoc.focus_set()

def addLn(s):
    txt.insert(tk.END, s + '\n')

def addParamLn(s, p):
    addLn(s + ' ' + p)

def addClick():
    p = pyautogui.position()
    addParamLn('Click', str(p.x) + ' ' + str(p.y))

def clearAll():
    txt.delete("1.0", "end")

def inputKey(event):
    focusobj = root.focus_get()
    if focusobj == txt:
        return

    key = event.keysym
    if key == 'c':
        addLn('Copy')
    elif key == 'a':
        addLn('SelAll')
    elif key == 'v':
        addLn('Paste')
    elif key == 'q':
        addClick()
    elif key == 'r':
        addLn('ResetPos')
    elif key == 'w':
        addParamLn('Wait', '50')
    elif key == 'F5':
        exec()
    else:
        if testMode:
            print(key)

def tkMain():
    global root
    global txt
    global buttonExe
    global buttonFoc

    root = tk.Tk()
    txt = tk.Text(
        width=28,
        height=18)

    buttonExe = tk.Button(
        root,
        text="EXE",
        width=28,
        height=2,
        command=exec)
    buttonFoc = tk.Button(
        root,
        text="FOC",
        width=28,
        height=2,
        command=foc)

    root.title("TKMacro")
    root.geometry('240x360')
    root.attributes("-topmost", True)
    root.bind("<KeyPress>", inputKey)

    buttonExe.pack()
    buttonFoc.pack()
    txt.pack()

    root.mainloop()


tkMain()
