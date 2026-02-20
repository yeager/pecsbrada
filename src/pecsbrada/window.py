"""Main window for PECS-bräda."""
import gettext
import subprocess
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, GdkPixbuf

from . import arasaac

_ = gettext.gettext

# Each entry: (emoji_fallback, translated_label, arasaac_search_term)
CATEGORIES = {
    _("Food"): [
        ("🍎", _("Apple"), "apple"), ("🍌", _("Banana"), "banana"),
        ("🥛", _("Milk"), "milk"), ("🍞", _("Bread"), "bread"),
        ("💧", _("Water"), "water"), ("🧃", _("Juice"), "juice"),
        ("🍪", _("Cookie"), "cookie"), ("🧀", _("Cheese"), "cheese"),
        ("🍕", _("Pizza"), "pizza"),
    ],
    _("Activities"): [
        ("🎮", _("Play"), "play"), ("📖", _("Read"), "read"),
        ("🎨", _("Draw"), "draw"), ("🎵", _("Music"), "music"),
        ("🏃", _("Run"), "run"), ("🧩", _("Puzzle"), "puzzle"),
        ("📺", _("TV"), "television"), ("🛝", _("Playground"), "playground"),
        ("🚗", _("Car ride"), "car"),
    ],
    _("Feelings"): [
        ("😊", _("Happy"), "happy"), ("😢", _("Sad"), "sad"),
        ("😠", _("Angry"), "angry"), ("😰", _("Worried"), "worried"),
        ("😴", _("Tired"), "tired"), ("🤗", _("Hug"), "hug"),
        ("😋", _("Hungry"), "hungry"), ("🥵", _("Hot"), "hot"),
        ("🥶", _("Cold"), "cold"),
    ],
    _("Actions"): [
        ("🚽", _("Toilet"), "toilet"), ("🖐️", _("Help"), "help"),
        ("✋", _("Stop"), "stop"), ("👋", _("Hello"), "hello"),
        ("🙏", _("Please"), "please"), ("❤️", _("Thank you"), "thank you"),
        ("➡️", _("More"), "more"), ("🚫", _("No"), "no"),
        ("✅", _("Yes"), "yes"),
    ],
}


class PecsbradaWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, default_width=600, default_height=700,
                         title=_("PECS-bräda"))
        self.current_category = list(CATEGORIES.keys())[0]
        self._build_ui()
        self._start_clock()

    def _build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # Header
        header = Adw.HeaderBar()
        main_box.append(header)

        theme_btn = Gtk.Button(icon_name="weather-clear-night-symbolic",
                               tooltip_text=_("Toggle dark/light theme"))
        theme_btn.connect("clicked", self._toggle_theme)
        header.pack_end(theme_btn)

        menu = Gio.Menu()
        menu.append(_("Preferences"), "app.preferences")
        menu.append(_("Keyboard Shortcuts"), "app.shortcuts")
        menu.append(_("About PECS-bräda"), "app.about")
        menu.append(_("Quit"), "app.quit")
        menu_btn = Gtk.MenuButton(icon_name="open-menu-symbolic", menu_model=menu)
        header.pack_end(menu_btn)

        # Sentence strip at top
        sentence_frame = Gtk.Frame()
        sentence_frame.set_margin_start(8)
        sentence_frame.set_margin_end(8)
        sentence_frame.set_margin_top(8)

        sentence_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        sentence_box.set_margin_start(8)
        sentence_box.set_margin_end(8)
        sentence_box.set_margin_top(8)
        sentence_box.set_margin_bottom(8)

        self.sentence_label = Gtk.Label(label=_("Tap images to build a sentence..."),
                                        xalign=0, hexpand=True, wrap=True)
        self.sentence_label.add_css_class("title-3")
        sentence_box.append(self.sentence_label)

        speak_btn = Gtk.Button(icon_name="audio-speakers-symbolic",
                               tooltip_text=_("Speak sentence"))
        speak_btn.add_css_class("suggested-action")
        speak_btn.connect("clicked", self._speak_sentence)
        sentence_box.append(speak_btn)

        clear_btn = Gtk.Button(icon_name="edit-clear-symbolic",
                               tooltip_text=_("Clear"))
        clear_btn.add_css_class("destructive-action")
        clear_btn.connect("clicked", self._clear_sentence)
        sentence_box.append(clear_btn)

        sentence_frame.set_child(sentence_box)
        main_box.append(sentence_frame)

        # Category tabs
        cat_box = Gtk.Box(spacing=0)
        cat_box.add_css_class("linked")
        cat_box.set_margin_start(8)
        cat_box.set_margin_end(8)
        cat_box.set_margin_top(8)
        first_btn = None
        for cat_name in CATEGORIES:
            btn = Gtk.ToggleButton(label=cat_name)
            if first_btn is None:
                first_btn = btn
                btn.set_active(True)
            else:
                btn.set_group(first_btn)
            btn.connect("toggled", self._on_category_changed, cat_name)
            cat_box.append(btn)
        main_box.append(cat_box)

        # Grid of PECS cards
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        self.grid = Gtk.FlowBox()
        self.grid.set_homogeneous(True)
        self.grid.set_max_children_per_line(4)
        self.grid.set_min_children_per_line(3)
        self.grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.grid.set_margin_start(8)
        self.grid.set_margin_end(8)
        self.grid.set_margin_top(8)
        scrolled.set_child(self.grid)
        main_box.append(scrolled)

        # Status
        self.status_label = Gtk.Label(label="", xalign=0)
        self.status_label.add_css_class("dim-label")
        self.status_label.set_margin_start(12)
        self.status_label.set_margin_bottom(4)
        main_box.append(self.status_label)

        self.sentence_words = []
        self._populate_grid()

    def _populate_grid(self):
        child = self.grid.get_first_child()
        while child:
            next_c = child.get_next_sibling()
            self.grid.remove(child)
            child = next_c

        items = CATEGORIES.get(self.current_category, [])
        provider = arasaac.get_provider()
        for emoji, label, term in items:
            btn = Gtk.Button()
            btn.set_size_request(120, 120)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            box.set_valign(Gtk.Align.CENTER)

            # Try ARASAAC pictogram, fall back to emoji
            icon_widget = None
            try:
                path = provider.get_pictogram(term, lang="en", resolution=96)
                if path:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        path, 64, 64, True)
                    icon_widget = Gtk.Image.new_from_pixbuf(pixbuf)
                    icon_widget.set_pixel_size(64)
            except Exception:
                pass
            if icon_widget is None:
                icon_widget = Gtk.Label(label=emoji)
                icon_widget.add_css_class("title-1")

            box.append(icon_widget)
            txt = Gtk.Label(label=label)
            txt.add_css_class("heading")
            box.append(txt)
            btn.set_child(box)
            btn.connect("clicked", self._on_pecs_clicked, emoji, label)
            self.grid.insert(btn, -1)

    def _on_category_changed(self, btn, cat_name):
        if btn.get_active():
            self.current_category = cat_name
            self._populate_grid()

    def _on_pecs_clicked(self, btn, emoji, label):
        self.sentence_words.append(label)
        display = " ".join(self.sentence_words)
        self.sentence_label.set_label(display)
        # Try TTS for single word
        self._speak(label)

    def _speak(self, text):
        try:
            subprocess.Popen(["espeak-ng", "-v", "sv", text],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            try:
                subprocess.Popen(["espeak", "-v", "sv", text],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                pass

    def _speak_sentence(self, btn):
        if self.sentence_words:
            self._speak(" ".join(self.sentence_words))

    def _clear_sentence(self, btn):
        self.sentence_words.clear()
        self.sentence_label.set_label(_("Tap images to build a sentence..."))

    def _toggle_theme(self, btn):
        mgr = Adw.StyleManager.get_default()
        if mgr.get_dark():
            mgr.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            mgr.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def _start_clock(self):
        GLib.timeout_add_seconds(1, self._update_clock)
        self._update_clock()

    def _update_clock(self):
        now = GLib.DateTime.new_now_local()
        self.status_label.set_label(now.format("%Y-%m-%d %H:%M:%S"))
        return True
