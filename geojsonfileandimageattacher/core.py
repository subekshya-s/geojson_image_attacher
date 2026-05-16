import os
import json
from difflib import get_close_matches


class GeoImageOrganizer:
    def __init__(self, input_geojson, image_folder, output_geojson, default_image="default.jpg"):
        self.input_geojson = input_geojson
        self.image_folder = image_folder
        self.output_geojson = output_geojson
        self.default_image = default_image

    def normalize(self, name):
        """Normalize string for matching"""
        return name.lower().replace(" ", "").replace("_", "").replace("-", "")

    def load_geojson(self):
        """Load GeoJSON file"""
        with open(self.input_geojson, "r") as f:
            return json.load(f)

    def get_image_mapping(self):
        """Create normalized image dictionary"""
        images = os.listdir(self.image_folder)
        return {
            self.normalize(os.path.splitext(img)[0]): img
            for img in images
        }

    def attach_images(self):
        """Main logic to attach images"""
        data = self.load_geojson()
        image_keys = self.get_image_mapping()

        for feature in data["features"]:
            name = feature["properties"].get("name", "")
            norm_name = self.normalize(name)

            match = get_close_matches(norm_name, image_keys.keys(), n=1, cutoff=0.6)

            if match:
                feature["properties"]["image"] = os.path.join(
                    self.image_folder, image_keys[match[0]]
                )
            else:
                feature["properties"]["image"] = os.path.join(
                    self.image_folder, self.default_image
                )

        return data

    def save_output(self, data):
        """Save updated GeoJSON"""
        with open(self.output_geojson, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Images attached. Output saved to {self.output_geojson}")

    def run(self):
        """Execute full pipeline"""
        data = self.attach_images()
        self.save_output(data)


# ---------------- USER INPUT ---------------- #
if __name__ == "__main__":
    print(" GeoJSON Image Organizer")

    input_geojson = input("Enter path to GeoJSON file: ")
    image_folder = input("Enter path to image folder: ")
    output_geojson = input("Enter output GeoJSON file name: ")

    default_choice = input("Enter default image name (or press Enter for 'default.jpg'): ")
    default_image = default_choice if default_choice else "default.jpg"

    organizer = GeoImageOrganizer(
        input_geojson,
        image_folder,
        output_geojson,
        default_image
    )

    organizer.run()



