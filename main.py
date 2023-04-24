import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer
import keyboard


class WordCounterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.word_count = 0
        self.misshit_count = 0
        self.time_left = 0
        self.running = False
        self.scores = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Word Counter")

        self.layout = QVBoxLayout()

        self.label = QLabel("Words per Minute: 0\nMisshit Count: 0\nTime Left: 0")
        self.layout.addWidget(self.label)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_countdown)
        self.layout.addWidget(self.start_button)

        self.reset_button = QPushButton("Reset Counter")
        self.reset_button.clicked.connect(self.reset_counter)
        self.layout.addWidget(self.reset_button)

        self.score_table = QLabel("Score Table:")
        self.layout.addWidget(self.score_table)

        self.setLayout(self.layout)

        self.monitor_key_presses()

    def start_countdown(self):
        self.reset_counter()
        self.start_button.setEnabled(False)
        self.reset_button.setEnabled(False)

        QTimer.singleShot(1000, lambda: self.label.setText("Starting in 3 seconds..."))
        QTimer.singleShot(2000, lambda: self.label.setText("Starting in 2 seconds..."))
        QTimer.singleShot(3000, lambda: self.label.setText("Starting in 1 second..."))
        QTimer.singleShot(4000, self.start_timer)

    def start_timer(self):
        self.running = True
        self.time_left = 60
        self.update_label()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)

    def stop_timer(self):
        self.running = False
        self.label.setText(f"Words per Minute: {self.word_count}\nMisshit Count: {self.misshit_count}\nTime Left: 0")
        self.start_button.setEnabled(True)
        self.reset_button.setEnabled(True)

    def update_label(self):
        if self.running:
            self.label.setText(
                f"Words per Minute: {self.word_count}\nMisshit Count: {self.misshit_count}\nTime Left: {self.time_left}")
            self.time_left -= 1
            if self.time_left == -1:
                self.timer.stop()
                self.stop_timer()

    def reset_counter(self):
        self.word_count = 0
        self.misshit_count = 0
        self.update_label()

    def on_key_press(self, e):
        if self.running:
            if e.name == 'space' or e.name == 'enter':
                self.word_count += 1
                self.update_label()
            elif e.name == 'backspace':
                self.misshit_count += 1
                self.update_label()

    def monitor_key_presses(self):
        keyboard.on_press(self.on_key_press)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    word_counter_app = WordCounterApp()
    word_counter_app.show()
    sys.exit(app.exec_())