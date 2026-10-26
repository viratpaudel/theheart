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
| `--preset` | Apply preconfigured visual theme | `classic`, `valentine`, `neon`, `cyberpunk`, `ruby`, `emerald`, `amber`, `twilight` |
| `--palette` | Choose color scheme index | `0` to `7` (Random if omitted) |
| `--speed` | Playback speed | `slow`, `normal`, `fast`, `instant` (Default: `normal`) |
| `--scale` | Scale factor for heart outline | `0.5` to `2.0` (Default: `1.0`) |
| `--message` | Custom center text / dedication | e.g. `"Happy Anniversary"` (Default: None) |
| `--sparkles` | Render twinkling ambient particle sparkles | Flag (Default: off) |
| `--pulse` | Rhythmic cardiac heartbeat pulsing cycle | Flag (Default: off) |
| `--bpm` | Heart rate in beats per minute for pulsing animation | `30` to `240` (Default: `60`) |
| `--family` | Filter words by linguistic family | `all`, `romance`, `germanic`, `slavic`, `asian`, `indic`, `african`, etc. |
| `--words` | Custom comma-separated words or path to file | e.g. `"Hope,Joy,Peace"` or `words.txt` |
| `--export-svg` | Headless export to vector SVG graphic | Path (e.g. `heart.svg`) |
| `--svg-gradient` | Apply smooth two-tone linear gradient to SVG export | Flag (Default: off) |
| `--export-json` | Export layout geometry, word coordinates, and angles to JSON | Path (e.g. `heart.json`) |

### Examples

**Instant Valentine theme with sparkles, pulse, and custom BPM:**
```bash
python heart.py --preset valentine --bpm 75
```

**Export vector SVG with dual-tone gradient fill:**
```bash
python heart.py --preset cyberpunk --export-svg heart.svg --svg-gradient
```

**Export heart geometry and multilingual layout coordinates to JSON:**
```bash
python heart.py --export-json layout.json
```

**Romance languages only with deep crimson theme:**
```bash
python heart.py --family romance --palette 4 --pulse
```

**Run with purple neon palette and fast animation:**
```bash
python heart.py --palette 2 --speed fast
```

**Run with instant rendering and a center message:**
```bash
python heart.py --speed instant --message "Forever & Always"
```

## Running Tests

Run the unit test suite locally:
```bash
python -m unittest discover -s tests
```

## Color Palettes

| Index | Background | Foreground | Theme |
|:-----:|:-----------|:-----------|:------|
| `0` | Black | `#ff4f91` | Classic Pink |
| `1` | Black | `#ff6b6b` | Coral |
| `2` | `#1a0a2e` | `#e040fb` | Neon Purple |
| `3` | `#0d1b2a` | `#00d4ff` | Cyber Cyan |
| `4` | `#1b0000` | `#ff2222` | Deep Crimson |
| `5` | `#051610` | `#10b981` | Emerald Night |
| `6` | `#190c00` | `#f59e0b` | Amber Glow |
| `7` | `#0a0a14` | `#818cf8` | Indigo Twilight |

## Controls

- **Click anywhere** on the canvas or press **`Esc`** / **`Q`** to close the window gracefully.

## License

This project is licensed under the [MIT License](LICENSE).
