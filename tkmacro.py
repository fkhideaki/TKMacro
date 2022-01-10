import tkinter as tk
import pyautogui
import time

import re

root = tk.Tk()
txt = tk.Text(width=30, height=20)

def execCmd(l):
    rr = re.match('([a-zA-Z]+) +(.+)', l)
    if not rr is None:
        cmd = rr.group(1)
        arg = rr.group(2)
        if cmd == 'Click':
            rr2 = re.match('([0-9]+) +([0-9]+)', arg)
            px = int(rr2.group(1))
            py = int(rr2.group(2))
            pyautogui.click(x=px, y=py, clicks=1, interval=0, button="left")
        elif cmd == 'Wait':
            wt = float(arg)
            time.sleep(wt * 0.001)
    else:
        cmd = l
        if cmd == 'Copy':
            pyautogui.hotkey("ctrl", "c")
        elif cmd == 'Paste':
            pyautogui.hotkey("ctrl", "v")
        elif cmd == 'SelAll':
            pyautogui.hotkey("ctrl", "a")

def exec():
    t = txt.get( "1.0", "end")
    v = t.splitlines()
    for l in v:
        execCmd(l)


def foc():
    buttonFoc.focus_set()

def addLn(s):
    txt.insert(tk.END, s + '\n')

def addClick():
    p = pyautogui.position()
    addLn('Click ' + str(p.x) + ' ' + str(p.y))

def addCmd(c):
    addLn(c)
    
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
    elif key == 'w':
        addLn('Wait ' + '100')
    elif key == 'F5':
        exec()
    elif key == 'Escape':
        clearAll()
    else:
        print(key)


buttonExe = tk.Button(
    root,
    text="EXE",
    command=exec)
buttonFoc = tk.Button(
    root,
    text="FOC",
    command=foc)

root.title("TKMacro")
root.geometry('300x350')
root.attributes("-topmost", True)
root.bind("<KeyPress>", inputKey)

buttonExe.pack()
buttonFoc.pack()
txt.pack()

root.mainloop()  
