# PECS-bräda

Digital PECS (Picture Exchange Communication System) board with text-to-speech.

> **Målgrupp / Target audience:** Barn och vuxna med autism, språkstörning (DLD),
> intellektuell funktionsnedsättning och andra kommunikationssvårigheter som behöver
> alternativ och kompletterande kommunikation (AKK/AAC). Perfekt för hemmet, skolan
> och habilitering.
>
> **For:** Children and adults with autism spectrum disorder (ASD), developmental
> language disorder (DLD), intellectual disabilities, and other communication
> difficulties who need augmentative and alternative communication (AAC). Ideal for
> home, school, and rehabilitation settings.

![Screenshot](screenshots/screenshot.png)

## Features

- Grid of pictograms organized by category (food, activities, feelings, actions)
- **ARASAAC pictogram integration** — automatically downloads free pictograms from
  [ARASAAC](https://arasaac.org) (CC BY-NC-SA, Government of Aragon / Sergio Palao)
- Emoji fallback when offline
- Tap image for TTS readout (via espeak-ng)
- Build sentences by tapping multiple images
- Customizable grid and categories
- Dark/light theme toggle

## Free Image Resources

| Resource | License | URL |
|----------|---------|-----|
| **ARASAAC** | CC BY-NC-SA 4.0 | https://arasaac.org |
| **OpenMoji** | CC BY-SA 4.0 | https://openmoji.org |
| **Mulberry Symbols** | CC BY-SA 2.0 UK | https://mulberrysymbols.org |
| **Sclera** | CC BY-NC 2.0 BE | https://sclera.be |

## Requirements

- Python 3.10+
- GTK4 / libadwaita
- PyGObject
- espeak-ng (for TTS)

## Installation

```bash
# Install dependencies (Fedora/RHEL)
sudo dnf install python3-gobject gtk4 libadwaita espeak-ng

# Install dependencies (Debian/Ubuntu)
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 espeak-ng

# Run from source
PYTHONPATH=src python3 -c "from pecsbrada.main import main; main()"
```

## ARASAAC Attribution

Pictographic symbols © Government of Aragon, created by Sergio Palao for
[ARASAAC](https://arasaac.org), distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## License

GPL-3.0-or-later

## Author

Daniel Nylander

## Links

- [GitHub](https://github.com/yeager/pecsbrada)
- [Issues](https://github.com/yeager/pecsbrada/issues)
- [Translations](https://app.transifex.com/danielnylander/pecsbrada)
