# PECS-bräda

Digital PECS (Picture Exchange Communication System) board with text-to-speech.

![Screenshot](screenshots/screenshot.png)

## Features

Grid of images (ARASAAC-compatible concept), tap image for TTS readout, customizable grid, categories (food, activities, feelings, actions). Build sentences by tapping.

## Requirements

- Python 3.10+
- GTK4 / libadwaita
- PyGObject

## Installation

```bash
# Install dependencies (Fedora/RHEL)
sudo dnf install python3-gobject gtk4 libadwaita

# Install dependencies (Debian/Ubuntu)
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1

# Run from source
PYTHONPATH=src python3 -c "from pecsbrada.main import main; main()"
```

## License

GPL-3.0-or-later

## Author

Daniel Nylander

## Links

- [GitHub](https://github.com/yeager/pecsbrada)
- [Issues](https://github.com/yeager/pecsbrada/issues)
- [Translations](https://app.transifex.com/danielnylander/pecsbrada)
