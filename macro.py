import tkinter as tk
import time
import threading
import pyautogui
import keyboard

class CoMacro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("")
        self.geometry("300x200")
        # 프레임 생성
        frame = tk.Frame(self)
        frame.pack(expand=True, padx=10, pady=10)

        # 프로그램 이름 레이블
        program_name_label = tk.Label(frame, text="수강신청 정정 매크로", font=("Helvetica", 20, 'bold'))
        program_name_label.grid(row=0, column=0, columnspan=2)
        
        explain1 = tk.Label(frame, text="r:좌표 기록 시작 e:좌표 기록 종료")
        explain1.grid(row=1, column=0, columnspan=2)

        explain2 = tk.Label(frame, text="s:매크로 시작 d:매크로 종료")
        explain2.grid(row=2, column=0, columnspan=2)

        self.x_label = tk.Label(frame, text="X:")
        self.x_label.grid(row=3, column=0, sticky="e")
        self.x_entry = tk.Entry(frame)
        self.x_entry.grid(row=3, column=1, sticky="we")

        self.y_label = tk.Label(frame, text="Y:")
        self.y_label.grid(row=4, column=0, sticky="e")
        self.y_entry = tk.Entry(frame)
        self.y_entry.grid(row=4, column=1, sticky="we")

        self.start_button = tk.Button(frame, text="Start", command=self.start_clicking)
        self.start_button.grid(row=5, column=0, columnspan=2, sticky="we")

        frame.grid_columnconfigure(1, weight=1)

        self.running = False
        self.clicking = False

        keyboard.add_hotkey('r', self.start_updating)
        keyboard.add_hotkey('e', self.stop_updating)
        keyboard.add_hotkey('s', self.start_clicking)
        keyboard.add_hotkey('d', self.stop_clicking)

    def start_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.clicking = True
            thread = threading.Thread(target=self.start_countdown)
            thread.start()

    def start_countdown(self):
        for i in range(3, 0, -1):
            self.start_button.config(text=f"{i}초 뒤 시작합니다.")
            time.sleep(1)
        self.start_button.config(text="매크로 시작")
        self.start_clicking_thread()

    def start_clicking_thread(self):
        while self.clicking:
            x = self.x_entry.get()
            y = self.y_entry.get()
            if x and y:
                pyautogui.click(int(x), int(y))
            time.sleep(0.7)

    def stop_clicking(self):
        self.clicking = False
        self.start_button.config(text="Start")

    def start_updating(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.update_coordinates)
            thread.start()

    def stop_updating(self):
        self.running = False

    def update_coordinates(self):
        while self.running:
            x, y = pyautogui.position()
            self.x_entry.delete(0, tk.END)
            self.x_entry.insert(0, x)
            self.y_entry.delete(0, tk.END)
            self.y_entry.insert(0, y)
            time.sleep(0.1)
            
app = CoMacro()
app.mainloop()
