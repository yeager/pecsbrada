# PECS-bräda

[![Version](https://img.shields.io/badge/version-0.2.0-blue)](https://github.com/yeager/pecsbrada/releases)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Transifex](https://img.shields.io/badge/Transifex-Translate-green.svg)](https://www.transifex.com/danielnylander/pecsbrada/)

Digital PECS (Picture Exchange Communication System) board with text-to-speech — GTK4/Adwaita.

> **For:** Children and adults with autism, DLD, or intellectual disabilities who use PECS for communication. Digital board with customizable cards and text-to-speech.

![Screenshot](screenshots/main.png)

## Features

- **PECS board** — customizable communication cards
- **Text-to-speech** — tap cards to hear words (espeak-ng)
- **ARASAAC pictograms** — automatic download of free symbols
- **Categories** — organize cards by topic
- **Custom cards** — add your own images and labels
- **Dark/light theme** toggle

## Installation

### Debian/Ubuntu

```bash
echo "deb [signed-by=/usr/share/keyrings/yeager-keyring.gpg] https://yeager.github.io/debian-repo stable main" | sudo tee /etc/apt/sources.list.d/yeager.list
curl -fsSL https://yeager.github.io/debian-repo/yeager-keyring.gpg | sudo tee /usr/share/keyrings/yeager-keyring.gpg > /dev/null
sudo apt update && sudo apt install pecsbrada
```

### Fedora/openSUSE

```bash
sudo dnf config-manager --add-repo https://yeager.github.io/rpm-repo/yeager.repo
sudo dnf install pecsbrada
```

### From source

```bash
git clone https://github.com/yeager/pecsbrada.git
cd pecsbrada && pip install -e .
pecsbrada
```

## ARASAAC Attribution

Pictographic symbols © Gobierno de Aragón, created by Sergio Palao for [ARASAAC](https://arasaac.org), distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Translation

Help translate on [Transifex](https://www.transifex.com/danielnylander/pecsbrada/).

## License

GPL-3.0-or-later — see [LICENSE](LICENSE) for details.

## Author

**Daniel Nylander** — [danielnylander.se](https://danielnylander.se)
