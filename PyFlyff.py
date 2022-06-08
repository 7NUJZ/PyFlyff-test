import json
import pathlib
import sys
import time

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon

from tkinter import Tk, Frame, Label, Entry, Button, X, W
from tkinter import messagebox

import threading

import win32gui
import win32con
import win32api

url = "https://universe.flyff.com/play"
icon = "icons/flyffu.ico"

activation_key = ""
in_game_key = ""
hwndMain = ""
repeat_times = 0
interval = 0

json_file = "AutoHotKey.json"
json_location = pathlib.Path("AutoHotKey.json")

start_autohotkey = False


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
        self.setWindowTitle("PyFlyff - Main")
        self.setWindowIcon(QIcon(icon))
        self.showMaximized()

        navbar = QToolBar()
        self.addToolBar(navbar)

        auto_hotkey = QAction("Set Auto Hotkey", self)
        auto_hotkey.triggered.connect(lambda: self.multithreading(self.auto_hotkey_config))
        navbar.addAction(auto_hotkey)

        self.reload_client = QShortcut(QKeySequence("Ctrl+Shift+F5"), self)
        self.reload_client.activated.connect(lambda: self.browser.setUrl(QUrl(url)))

        self.change_fullscreen = QShortcut(QKeySequence("Ctrl+Shift+F11"), self)
        self.change_fullscreen.activated.connect(lambda: self.fullscreen(MainWindow))

        self.new_client = QShortcut(QKeySequence("Ctrl+Shift+PgUp"), self)
        self.new_client.activated.connect(self.create_new_window)

        self.autoKey = QShortcut(self)
        self.autoKey.activated.connect(self.start_auto_hotkey)

        self.break_auto_hotkey_loop = QShortcut(QKeySequence("End"), self)
        self.break_auto_hotkey_loop.activated.connect(self.stop_auto_hotkey)

        self.windows = []

    def set_short_cut(self, shortcut):
        self.autoKey.setKey(shortcut)

    @staticmethod
    def auto_key_press():
        global start_autohotkey
        global hwndMain
        global in_game_key

        counter = 0

        try:
            while True:

                if counter < repeat_times and start_autohotkey is True:

                    win32api.SendMessage(hwndMain, win32con.WM_KEYDOWN, in_game_key, 0)
                    time.sleep(0.5)
                    win32api.SendMessage(hwndMain, win32con.WM_KEYUP, in_game_key, 0)

                    time.sleep(interval)

                    counter += 1
                else:
                    break
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def stop_auto_hotkey():
        global start_autohotkey

        start_autohotkey = False

    def start_auto_hotkey(self):
        global start_autohotkey
        global hwndMain

        hwndMain = win32gui.FindWindow(None, "PyFlyff - Main")

        if not start_autohotkey:
            start_autohotkey = True
            self.multithreading(self.auto_key_press)

    def auto_hotkey_config(self):

        global activation_key
        global in_game_key
        global repeat_times
        global interval

        hotkey_window_config = Tk()

        window_width = 250
        window_height = 140

        screen_width = hotkey_window_config.winfo_screenwidth()
        screen_height = hotkey_window_config.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        hotkey_window_config.geometry("250x170+" + str(int(x)) + "+" + str(int(y)))
        hotkey_window_config.resizable(False, False)
        hotkey_window_config.title("Config")
        hotkey_window_config.iconbitmap("icons/flyffu.ico")

        def save():
            global activation_key
            global in_game_key
            global repeat_times
            global interval

            vk_code = {'backspace': 0x08,
                       'tab': 0x09,
                       'clear': 0x0C,
                       'enter': 0x0D,
                       'shift': 0x10,
                       'ctrl': 0x11,
                       'alt': 0x12,
                       'pause': 0x13,
                       'caps_lock': 0x14,
                       'esc': 0x1B,
                       'spacebar': 0x20,
                       'page_up': 0x21,
                       'page_down': 0x22,
                       'end': 0x23,
                       'home': 0x24,
                       'left_arrow': 0x25,
                       'up_arrow': 0x26,
                       'right_arrow': 0x27,
                       'down_arrow': 0x28,
                       'select': 0x29,
                       'print': 0x2A,
                       'execute': 0x2B,
                       'print_screen': 0x2C,
                       'ins': 0x2D,
                       'del': 0x2E,
                       'help': 0x2F,
                       '0': 0x30,
                       '1': 0x31,
                       '2': 0x32,
                       '3': 0x33,
                       '4': 0x34,
                       '5': 0x35,
                       '6': 0x36,
                       '7': 0x37,
                       '8': 0x38,
                       '9': 0x39,
                       'a': 0x41,
                       'b': 0x42,
                       'c': 0x43,
                       'd': 0x44,
                       'e': 0x45,
                       'f': 0x46,
                       'g': 0x47,
                       'h': 0x48,
                       'i': 0x49,
                       'j': 0x4A,
                       'k': 0x4B,
                       'l': 0x4C,
                       'm': 0x4D,
                       'n': 0x4E,
                       'o': 0x4F,
                       'p': 0x50,
                       'q': 0x51,
                       'r': 0x52,
                       's': 0x53,
                       't': 0x54,
                       'u': 0x55,
                       'v': 0x56,
                       'w': 0x57,
                       'x': 0x58,
                       'y': 0x59,
                       'z': 0x5A,
                       'numpad_0': 0x60,
                       'numpad_1': 0x61,
                       'numpad_2': 0x62,
                       'numpad_3': 0x63,
                       'numpad_4': 0x64,
                       'numpad_5': 0x65,
                       'numpad_6': 0x66,
                       'numpad_7': 0x67,
                       'numpad_8': 0x68,
                       'numpad_9': 0x69,
                       'multiply_key': 0x6A,
                       'add_key': 0x6B,
                       'separator_key': 0x6C,
                       'subtract_key': 0x6D,
                       'decimal_key': 0x6E,
                       'divide_key': 0x6F,
                       'F1': 0x70,
                       'F2': 0x71,
                       'F3': 0x72,
                       'F4': 0x73,
                       'F5': 0x74,
                       'F6': 0x75,
                       'F7': 0x76,
                       'F8': 0x77,
                       'F9': 0x78,
                       'F10': 0x79,
                       'F11': 0x7A,
                       'F12': 0x7B,
                       'F13': 0x7C,
                       'F14': 0x7D,
                       'F15': 0x7E,
                       'F16': 0x7F,
                       'F17': 0x80,
                       'F18': 0x81,
                       'F19': 0x82,
                       'F20': 0x83,
                       'F21': 0x84,
                       'F22': 0x85,
                       'F23': 0x86,
                       'F24': 0x87,
                       'num_lock': 0x90,
                       'scroll_lock': 0x91,
                       'left_shift': 0xA0,
                       'right_shift ': 0xA1,
                       'left_control': 0xA2,
                       'right_control': 0xA3,
                       'left_menu': 0xA4,
                       'right_menu': 0xA5,
                       'browser_back': 0xA6,
                       'browser_forward': 0xA7,
                       'browser_refresh': 0xA8,
                       'browser_stop': 0xA9,
                       'browser_search': 0xAA,
                       'browser_favorites': 0xAB,
                       'browser_start_and_home': 0xAC,
                       'volume_mute': 0xAD,
                       'volume_Down': 0xAE,
                       'volume_up': 0xAF,
                       'next_track': 0xB0,
                       'previous_track': 0xB1,
                       'stop_media': 0xB2,
                       'play/pause_media': 0xB3,
                       'start_mail': 0xB4,
                       'select_media': 0xB5,
                       'start_application_1': 0xB6,
                       'start_application_2': 0xB7,
                       'attn_key': 0xF6,
                       'crsel_key': 0xF7,
                       'exsel_key': 0xF8,
                       'play_key': 0xFA,
                       'zoom_key': 0xFB,
                       'clear_key': 0xFE,
                       '+': 0xBB,
                       ',': 0xBC,
                       '-': 0xBD,
                       '.': 0xBE,
                       '/': 0xBF,
                       '`': 0xC0,
                       ';': 0xBA,
                       '[': 0xDB,
                       '\\': 0xDC,
                       ']': 0xDD,
                       "'": 0xDE}

            try:
                if (
                        activation_key_entry.get() and in_game_hotkey_entry.get() and repeat_times_entry.get() and interval_entry.get()) == "":
                    messagebox.showerror("Error", "Fields cannot be empty.")
                elif activation_key_entry.get() == in_game_hotkey_entry.get():
                    messagebox.showerror("Error", "Activate Key and Pressed Key must be different.")
                else:

                    self.create_json_config(activation_key_entry.get(), in_game_hotkey_entry.get(),
                                            repeat_times_entry.get(), interval_entry.get())

                    activation_key = activation_key_entry.get()
                    in_game_key = vk_code.get(in_game_hotkey_entry.get())
                    repeat_times = int(repeat_times_entry.get())
                    interval = int(interval_entry.get())

                    self.set_short_cut(activation_key)

                    hotkey_window_config.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        frame = Frame()

        frame.pack(fill=X, padx=5, pady=5)

        activation_key_label = Label(frame, text="Activation Key:", width=15, anchor=W)
        activation_key_entry = Entry(frame, width=20)

        in_game_hotkey_label = Label(frame, text="In-game Hotkey:", width=15, anchor=W)
        in_game_hotkey_entry = Entry(frame, width=20)

        repeat_times_label = Label(frame, text="Repeat:", width=15, anchor=W)
        repeat_times_entry = Entry(frame, width=20)

        interval_label = Label(frame, text="Interval:", width=15, anchor=W)
        interval_entry = Entry(frame, width=20)

        activation_key_label.grid(row=0, column=0, pady=5)
        activation_key_entry.grid(row=0, column=1, pady=5)

        in_game_hotkey_label.grid(row=1, column=0, pady=5)
        in_game_hotkey_entry.grid(row=1, column=1, pady=5)

        repeat_times_label.grid(row=2, column=0, pady=5)
        repeat_times_entry.grid(row=2, column=1, pady=5)

        interval_label.grid(row=3, column=0, pady=5)
        interval_entry.grid(row=3, column=1, pady=5)

        button_save = Button(text="Save", width=10, height=1, command=save)
        button_save.pack()

        try:
            if json_location.exists():
                with open(json_location) as js:
                    data = json.load(js)

                    activation_key_entry.insert(0, data["activation_key"])
                    in_game_hotkey_entry.insert(0, data["in_game_key"])
                    repeat_times_entry.insert(0, data["repeat_times"])
                    interval_entry.insert(0, data["interval"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

        hotkey_window_config.mainloop()

    @staticmethod
    def multithreading(function):
        threading.Thread(target=function).start()

    def create_new_window(self):
        self.new_window = QWebEngineView()
        self.new_window.load(QUrl(url))
        self.new_window.setWindowTitle("PyFlyff - Alt")
        self.new_window.setWindowIcon(QIcon(icon))
        self.new_window.showMaximized()

        self.windows.append(self.new_window)

    def fullscreen(self, w):
        if w.isFullScreen(self):
            w.showMaximized(self)
        else:
            w.showFullScreen(self)

    @staticmethod
    def create_json_config(value1, value2, value3, value4):

        try:
            data = {"activation_key": value1, "in_game_key": value2, "repeat_times": value3,
                    "interval": value4}

            json_data = json.dumps(data)

            save_json = open(json_file, "w")
            save_json.write(str(json_data))
            save_json.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec_()
