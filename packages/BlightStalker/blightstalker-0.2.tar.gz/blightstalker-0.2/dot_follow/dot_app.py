import tkinter as tk
import ctypes
from ctypes import wintypes

class Blight:
    def __init__(self):
        self.root = tk.Tk()
        self.dot_radius = 10
        self.dot_x = self.root.winfo_screenwidth() // 2
        self.dot_y = self.root.winfo_screenheight() // 2
        self.dot = None
        self.dot_visible = True

    def run(self):
        self.setup_window()
        self.setup_dot()
        self.update_dot_position()
        self.setup_key_bindings()
        self.root.mainloop()

    def setup_window(self):
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.attributes('-transparentcolor', 'black')
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        self.enable_aero(hwnd)
        self.make_click_through(hwnd)

    def setup_dot(self):
        canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.dot = canvas.create_oval(
            self.dot_x - self.dot_radius, self.dot_y - self.dot_radius,
            self.dot_x + self.dot_radius, self.dot_y + self.dot_radius,
            fill='aqua', outline='red', width=5
        )

    def enable_aero(self, window_id):
        dwmapi = ctypes.windll.dwmapi
        DWMWA_TRANSITIONS_FORCEDISABLED = 3
        DWMWA_ALLOW_NCPAINT = 4
        DWM_BB_ENABLE = 1
        DWM_BB_BLURREGION = 2
        class DWM_BLURBEHIND(ctypes.Structure):
            _fields_ = [
                ("dwFlags", ctypes.wintypes.DWORD),
                ("fEnable", ctypes.wintypes.BOOL),
                ("hRgnBlur", ctypes.wintypes.HRGN),
                ("fTransitionOnMaximized", ctypes.wintypes.BOOL),
            ]
        bb = DWM_BLURBEHIND()
        bb.dwFlags = DWM_BB_ENABLE | DWM_BB_BLURREGION
        bb.fEnable = True
        bb.hRgnBlur = None
        bb.fTransitionOnMaximized = False
        dwmapi.DwmEnableBlurBehindWindow(window_id, ctypes.byref(bb))
        dwmapi.DwmSetWindowAttribute(window_id, DWMWA_TRANSITIONS_FORCEDISABLED, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))
        dwmapi.DwmSetWindowAttribute(window_id, DWMWA_ALLOW_NCPAINT, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))

    def make_click_through(self, window_id):
        style = ctypes.windll.user32.GetWindowLongW(window_id, -20)  # -20 corresponds to GWL_EXSTYLE
        style |= 0x80000 | 0x20  # WS_EX_LAYERED | WS_EX_TRANSPARENT
        ctypes.windll.user32.SetWindowLongW(window_id, -20, style)
        ctypes.windll.user32.SetLayeredWindowAttributes(window_id, 0, 0, 1)

    def update_dot_position(self):
        if self.dot_visible:
            mouse_x, mouse_y = self.root.winfo_pointerxy()
            self.dot_x += (mouse_x - self.dot_x) * 0.1
            self.dot_y += (mouse_y - self.dot_y) * 0.1
            canvas = self.root.children["!canvas"]
            canvas.coords(self.dot, self.dot_x - self.dot_radius, self.dot_y - self.dot_radius,
                          self.dot_x + self.dot_radius, self.dot_y + self.dot_radius)
        self.root.after(10, self.update_dot_position)

    def toggle_dot_visibility(self, event=None):
        self.dot_visible = not self.dot_visible
        canvas = self.root.children["!canvas"]
        if self.dot_visible:
            canvas.itemconfig(self.dot, state="normal")
        else:
            canvas.itemconfig(self.dot, state="hidden")

    def setup_key_bindings(self):
        self.root.bind("<Control-Alt-d>", self.toggle_dot_visibility)
def Blight_init():
    if __name__ == "__main__":
        app = Blight()
        app.run()
