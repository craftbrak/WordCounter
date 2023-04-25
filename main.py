import gi

gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, GLib, Adw
import keyboard
from threading import Thread


class WordCounterApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.WordCounterApp")

    def do_startup(self):
        Adw.Application.do_startup(self)

    def do_activate(self):
        app_window = Gtk.ApplicationWindow(application=self)
        self.window = Gtk.Window()
        app_window.set_transient_for(self.window)

        self.window.set_title("Word Counter")

        self.word_count = 0
        self.misshit_count = 0
        self.time_left = 0
        self.running = False
        self.scores = []

        self.label = Gtk.Label(label="Words per Minute: 0\nMisshit Count: 0\nTime Left: 0", wrap=True)
        self.start_button = Gtk.Button.new_with_label("Start")
        self.start_button.connect("clicked", self.start_countdown)
        self.reset_button = Gtk.Button.new_with_label("Reset Counter")
        self.reset_button.connect("clicked", self.reset_counter)

        self.score_table = Gtk.Label(label="Score Table:")

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        grid.attach(self.label, 0, 0, 2, 1)
        grid.attach(self.start_button, 0, 1, 1, 1)
        grid.attach(self.reset_button, 1, 1, 1, 1)
        grid.attach(self.score_table, 0, 2, 2, 1)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(grid)
        self.window.set_child(box)
        self.window.present()

        self.monitor_key_presses()

    def start_countdown(self, button):
        self.reset_counter()
        self.start_button.set_sensitive(False)
        self.reset_button.set_sensitive(False)
        self.label.set_text("Starting in 4 seconds...")
        GLib.timeout_add(1000, self.update_starting_label, 3)

    def update_starting_label(self, count):
        if count == 0:
            self.label.set_text("Starting...")
            GLib.timeout_add(1000, self.start_timer)
        else:
            self.label.set_text(f"Starting in {count} seconds...")
            GLib.timeout_add(1000, self.update_starting_label, count - 1)

    def start_timer(self):
        self.running = True
        self.time_left = 60
        self.update_label()
        GLib.timeout_add(60000, self.stop_timer)
        GLib.timeout_add(1000, self.update_time_left)

    def stop_timer(self):
        self.running = False
        self.scores.append((self.word_count, self.misshit_count))
        self.update_label()
        self.update_score_table()
        self.start_button.set_sensitive(True)
        self.reset_button.set_sensitive(True)

    def update_label(self):
        self.label.set_text(
            f"Words per Minute: {self.word_count}\nMisshit Count: {self.misshit_count}\nTime Left: {self.time_left}")

    def update_time_left(self):
        if self.running:
            self.time_left -= 1
            self.update_label()
            GLib.timeout_add(1000, self.update_time_left)

    def reset_counter(self, button=None):
        self.word_count = 0
        self.misshit_count = 0
        self.update_label()

    def update_score_table(self):
        score_table_text = "Score Table:\n"
        for idx, score in enumerate(self.scores, start=1):
            score_table_text += f"{idx}. Words: {score[0]}, Misshits: {score[1]}\n"
        self.score_table.set_text(score_table_text)

    def on_key_press(self, e):
        if self.running:
            if e.name == 'space' or e.name == 'enter':
                self.word_count += 1
                self.update_label()
            elif e.name == 'backspace':
                self.misshit_count += 1
                self.update_label()

    def on_close(self, window):
        self.running = False
        Adw.main_quit()

    def monitor_key_presses(self):
        keyboard.on_press(self.on_key_press)
        self.window.connect("destroy", self.on_close)


if __name__ == "__main__":
    app = WordCounterApp()
    app.run()
