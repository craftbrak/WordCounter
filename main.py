import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import keyboard

class WordCounterApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Word Counter")

        self.word_count = 0
        self.misshit_count = 0
        self.time_left = 0
        self.running = False
        self.scores = []

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.label = Gtk.Label(label="Words per Minute: 0\nMisshit Count: 0\nTime Left: 0", xalign=0)
        vbox.pack_start(self.label, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.start_countdown)
        hbox.pack_start(self.start_button, True, True, 0)

        self.reset_button = Gtk.Button(label="Reset Counter")
        self.reset_button.connect("clicked", self.reset_counter)
        hbox.pack_start(self.reset_button, True, True, 0)

        self.score_table = Gtk.Label(label="Score Table:", xalign=0)
        vbox.pack_start(self.score_table, True, True, 0)

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
        self.label.set_text(f"Words per Minute: {self.word_count}\nMisshit Count: {self.misshit_count}\nTime Left: {self.time_left}")

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

    def run(self):
        self.show_all()
        Gtk.main()

    def on_close(self, window):
        self.running = False
        Gtk.main_quit()

    def monitor_key_presses(self):
        keyboard.on_press(self.on_key_press)
        self.connect("delete-event", self.on_close)

if __name__ == "__main__":
    app = WordCounterApp()
    app.run()