# 🗺️ GeoImage Organizer

A Python utility that automatically attaches images to GeoJSON features based on name matching.  
It uses fuzzy string matching to intelligently link spatial features with corresponding image files.

---

## 🚀 Features

- Reads GeoJSON files
- Matches feature names with image filenames
- Uses fuzzy matching for better accuracy
- Attaches image paths to GeoJSON properties
- Supports default image fallback
- Outputs updated GeoJSON file

---

## 🧠 How It Works

1. Load GeoJSON file
2. Read all images from a folder
3. Normalize names (lowercase, remove spaces/symbols)
4. Match feature names with image filenames using fuzzy matching
5. Attach best-matching image path to each feature
6. Save updated GeoJSON

---

## 📁 Project Structure
project/
│
├── geo_image_organizer.py # Main script
├── input.geojson # Input GeoJSON file
├── images/ # Image folder
│ ├── kathmandu.jpg
│ ├── pokhara.jpg
│ └── default.jpg
└── output.geojson # Output file (generated)



---

## ⚙️ Requirements

- Python 3.7+
- No external libraries required (uses built-in modules only)

---

## 📦 Standard Libraries Used

- os
- json
- difflib (get_close_matches)

---

## ▶️ How to Run

```bash
python geo_image_organizer.py
pip install setuptools wheel twine

