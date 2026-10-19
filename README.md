# 💖 The Heart

A beautiful animated heart drawn with Python's `turtle` graphics, featuring the word **"love"** written in **50 different languages** around the outline.

## Requirements

- Python 3.8+
- `turtle` & `tkinter` (included in standard Python distributions)

## Quick Start

Run with default settings:
```bash
python heart.py
```

## CLI Options

| Flag | Description | Options / Defaults |
|------|-------------|---------------------|
| `--palette` | Choose color scheme index | `0` to `4` (Random if omitted) |
| `--speed` | Playback speed | `slow`, `normal`, `fast`, `instant` (Default: `normal`) |
| `--scale` | Scale factor for heart outline | `0.5` to `2.0` (Default: `1.0`) |
| `--message` | Custom center text / dedication | e.g. `"Happy Anniversary"` (Default: None) |

### Examples

**Run with purple neon palette and fast animation:**
```bash
python heart.py --palette 2 --speed fast
```

**Run with instant rendering and a center message:**
```bash
python heart.py --speed instant --message "Forever & Always"
```

## Color Palettes

| Index | Background | Foreground | Theme |
|:-----:|:-----------|:-----------|:------|
| `0` | Black | `#ff4f91` | Classic Pink |
| `1` | Black | `#ff6b6b` | Coral |
| `2` | `#1a0a2e` | `#e040fb` | Neon Purple |
| `3` | `#0d1b2a` | `#00d4ff` | Cyber Cyan |
| `4` | `#1b0000` | `#ff2222` | Deep Crimson |

## Controls

- **Click anywhere** on the canvas or press **`Esc`** / **`Q`** to close the window gracefully.

## License

This project is licensed under the [MIT License](LICENSE).
