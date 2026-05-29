# 🗺️ GeoJSON Image Organizer

[![PyPI version](https://badge.fury.io/py/geojsonfile-image-attacher.svg)](https://badge.fury.io/py/geojsonfile-image-attacher)
[![Python](https://img.shields.io/pypi/pyversions/geojsonfile-image-attacher)](https://pypi.org/project/geojsonfile-image-attacher/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-8%20passed-brightgreen)](https://github.com/subekshya-s/geojson_image_attacher)

A Python package that automatically attaches images to GeoJSON features based on name matching.
It uses fuzzy string matching to intelligently link spatial features with corresponding image files —
even when names are slightly different, misspelled, or formatted inconsistently.

---

## ✨ Features

- Reads GeoJSON files and matches features to images automatically
- Uses **fuzzy matching** (rapidfuzz) for intelligent name linking
- Normalizes names — handles spaces, hyphens, underscores, and case differences
- Returns `null` honestly when no image matches — no silent fallbacks
- Exports a **CSV report** of unmatched features
- Configurable match sensitivity with `--cutoff`
- Full **CLI support** — use it directly from terminal
- Supports jpg, jpeg, png, webp, gif image formats

---

## 🧠 How It Works

```
GeoJSON features          Image folder
─────────────────         ─────────────
"Kathmandu"    ──fuzzy──▶  kathmandu.jpg   ✅ matched
"Patan Durbar" ──fuzzy──▶  patan-durbar.jpg ✅ matched
"XYZ Place"    ──no match─▶ null            ⚠️ reported
```

1. Load GeoJSON file
2. Read all images from folder
3. Normalize names (lowercase, remove spaces/symbols)
4. Match feature names to image filenames using fuzzy matching
5. Attach best-matching image path to each feature
6. Save updated GeoJSON + optional CSV report of unmatched features

---

## 📁 Project Structure

```
project/
│
├── geojsonfileandimageattacher/
│   ├── __init__.py
│   ├── core.py           # Main logic
│   └── cli.py            # CLI interface
│
├── tests/
│   └── test_core.py      # Full test suite
│
├── demo/
│   ├── input.geojson     # Sample input
│   ├── images/           # Sample images
│   └── output.geojson    # Generated output
│
├── setup.py
├── pyproject.toml
└── README.md
```

---

## ⚙️ Requirements

- Python 3.6+
- rapidfuzz

---

## 📦 Installation

```bash
pip install geojsonfile_image_attacher
```

Or for local development:

```bash
git clone https://github.com/subekshya-s/geojson_image_attacher.git
cd geojson_image_attacher
pip install -e .
```

---

## ▶️ Usage

### CLI (recommended)

```bash
# Basic usage
geojson-attach --input map.geojson --images ./photos --output result.geojson

# Stricter matching (default is 75)
geojson-attach --input map.geojson --images ./photos --output result.geojson --cutoff 85

# With CSV report of unmatched features
geojson-attach --input map.geojson --images ./photos --output result.geojson --report

# Help
geojson-attach --help
```

### Python API

```python
from geojsonfileandimageattacher import GeoImageOrganizer

organizer = GeoImageOrganizer(
    input_geojson="input.geojson",
    image_folder="images/",
    output_geojson="output.geojson",
    cutoff=75           # match sensitivity 0-100
)

organizer.run()
```

---

## 📊 Output Example

Input feature:
```json
{
  "type": "Feature",
  "properties": {
    "name": "Kathmandu"
  }
}
```

Output feature:
```json
{
  "type": "Feature",
  "properties": {
    "name": "Kathmandu",
    "image": "images/kathmandu.jpg",
    "image_match_score": 100.0
  }
}
```

Unmatched feature:
```json
{
  "type": "Feature",
  "properties": {
    "name": "Unknown Place",
    "image": null,
    "image_match_score": 0
  }
}
```

---

## 📄 CSV Report (--report flag)

When `--report` is used, a CSV file is generated next to your output:

```
feature_name,status
Bhaktapur,no image found
Unknown Place XYZ,no image found
```

---

## 🖼️ Screenshots

> _Add screenshots here after running on demo data_
>
> Example:
> ```
> 🗺️  GeoJSON Image Organizer
>    Input:   demo/input.geojson
>    Images:  demo/images
>    Output:  demo/output.geojson
>    Cutoff:  75
>
> 📊 Results: 5/8 features matched
>
> ⚠️  No image found for:
>    - Bhaktapur
>    - Unknown Place XYZ
>    - [unnamed feature]
>
> 💾 Output saved to demo/output.geojson
> 📄 Report saved to demo/output_unmatched.csv
> ```

---

## 🧪 Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

Expected output:
```
test_normalize                         PASSED ✅
test_get_image_mapping                 PASSED ✅
test_attach_images_with_match          PASSED ✅
test_attach_images_no_match            PASSED ✅
test_save_output                       PASSED ✅
test_missing_geojson_raises_error      PASSED ✅
test_missing_image_folder_raises_error PASSED ✅
test_invalid_json_raises_error         PASSED ✅
```

---

## 🔧 CLI Options

| Option | Required | Default | Description |
|---|---|---|---|
| `--input` | ✅ | — | Path to input GeoJSON file |
| `--images` | ✅ | — | Path to image folder |
| `--output` | ✅ | — | Path to output GeoJSON file |
| `--cutoff` | ❌ | 75 | Match sensitivity 0-100 |
| `--report` | ❌ | False | Export unmatched CSV report |

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author

**Subekshya Subedi**
- GitHub: [@subekshya-s](https://github.com/subekshya-s)
- Email: subekshyasubedi26@gmail.com

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

```bash
git clone https://github.com/subekshya-s/geojson_image_attacher.git
pip install -e .
python -m pytest tests/ -v
```