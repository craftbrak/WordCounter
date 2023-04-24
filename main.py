import tkinter as tk
import keyboard
from threading import Thread


class WordCounterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Word Counter")

        self.word_count = 0
        self.misshit_count = 0
        self.time_left = 0
        self.running = False
        self.scores = []

        self.label = tk.Label(self.root, text="Words per Minute: 0\nMisshit Count: 0\nTime Left: 0", font=("Arial", 18),
                              justify=tk.LEFT)
        self.label.pack(anchor='center', pady=20)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(self.root, text="Reset Counter", command=self.reset_counter)
        self.reset_button.pack(side=tk.RIGHT, padx=10)

        self.score_table = tk.Label(self.root, text="Score Table:", font=("Arial", 14), justify=tk.LEFT)
        self.score_table.pack(anchor='center', pady=10)

        self.monitor_key_presses()

    def start_countdown(self):
        self.reset_counter()
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.label.config(text="Starting in 4 seconds...")
        self.root.after(1000, lambda: self.label.config(text="Starting in 3 seconds..."))
        self.root.after(2000, lambda: self.label.config(text="Starting in 2 seconds..."))
        self.root.after(3000, lambda: self.label.config(text="Starting in 1 second..."))
        self.root.after(4000, self.start_timer)

    def start_timer(self):
        self.running = True
        self.time_left = 60
        self.update_score_label()
        self.update_time_label()
        self.root.after(60000, self.stop_timer)

    def stop_timer(self):
        self.running = False
        self.scores.append((self.word_count, self.misshit_count))
        self.label.config(
            text=f"Words per Minute: {self.word_count}\nMisshit Count: {self.misshit_count}\nTime Left: 0")
        self.update_score_table()
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def update_score_label(self):
        if self.running:
            self.label.config(
                text=f"Words per Minute: {self.word_count}\nMisshit Count: {self.misshit_count}\nTime Left: {self.time_left}")
            self.root.after(1000, self.update_score_label)

    def update_time_label(self):
        if self.running:
            self.root.after(1000, self.update_time_label)
            self.time_left -= 1

    def reset_counter(self):
        self.word_count = 0
        self.misshit_count = 0
        self.update_score_label()

    def update_score_table(self):
        score_table_text = "Score Table:\n"
        for idx, score in enumerate(self.scores, start=1):
            score_table_text += f"{idx}. Words: {score[0]}, Misshits: {score[1]}\n"
        self.score_table.config(text=score_table_text)

    def on_key_press(self, e):
        if self.running:
            if e.name == 'space' or e.name == 'enter':
                self.word_count += 1
                self.update_score_label()
            elif e.name == 'backspace':
                self.misshit_count += 1
                self.update_score_label()

    def monitor_key_presses(self):
        keyboard.on_press(self.on_key_press)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WordCounterApp()
    app.run()
