import os
import json
from rapidfuzz import process,fuzz


class GeoImageOrganizer:
    def __init__(self, input_geojson, image_folder, output_geojson,cutoff=75):
        self.input_geojson = input_geojson
        self.image_folder = image_folder
        self.output_geojson = output_geojson
        self.cutoff = cutoff
        

    def normalize(self, name):
        """Normalize string for matching"""
        return name.lower().replace(" ", "").replace("_", "").replace("-", "")

    def validate_inputs(self):
        """check all the input before doing anything.Fails early with the clear messages"""
        if not os.path.exists(self.input_geojson):
            raise FileNotFoundError(
                f"GEOJSON file not found at '{self.input_geojson}'\n"
                f"Please check the path and try again ."
            )
        #check its actually a .geojson or .json file
        if not self.input_geojson.endswith((".geojson",".json")):
            raise ValueError(f"'{self.input_geojson}' is not a valid GeoJson file.\n"f"File must end with .geojson or .json")

        if not os.path.exists(self.image_folder):
            raise FileNotFoundError(f"Image folder not found at '{self.image_folder}'\n" f"Please check the path and try again.")
        
        #Check image folder is not empty
        images = os.listdir(self.image_folder)
        if not images :
            raise ValueError(f"Image folder '{self.image_folder}' is empty.\n" f"Please  add images before running.")


    def load_geojson(self):
        """Load and validate GeoJSON file"""
        with open(self.input_geojson, "r") as f:
            try :
                data = json.load(f)
            except json.JSONDecodeError as e :
                raise ValueError(
                    f"Could not read '{self.input_geojson}' - invalid JSON.\n" f"Details:{e}")
                
        if "features" not in data:
            raise ValueError(
                f"'{self.input_geojson}' is not a valid GEOJSON file.\n" f"MIssing 'features' key."
            )
        
        if len(data["features"]) == 0:
               raise ValueError(
                   f"'{self.input_geojson}' has no features to process."
               )
        return data

    def get_image_mapping(self):
        """Create normalized image dictionary"""
        images = os.listdir(self.image_folder)
        valid_extensions = (".jpg",".jpeg",".png",".webp",".gif")
        images = [img for img in images if img.lower().endswith(valid_extensions)]

        if not images:
            raise ValueError(
                f"No valid image files found in '{self.image_folder}' .\n" f"Supported formats: jpg.jpeg,png,webp,gif")
            
        return {
            self.normalize(os.path.splitext(img)[0]): img
            for img in images
        }
    
    def find_best_match(self,norm_name,image_keys):
        """Use rapidfuzz to find best_matching image key. Returns matched key and score or (None,0) if no match."""
        result = process.extractOne(
            norm_name,
            image_keys,
            scorer=fuzz.WRatio,
            score_cutoff=self.cutoff)
        
        if result:
            matched_key, score, _=result
            return matched_key,score
        return None,0

        

    def attach_images(self):
        """Main logic to attach images"""
        data = self.load_geojson()
        image_keys = self.get_image_mapping()
        unmatched = []
        for feature in data["features"]:
            name = feature["properties"].get("name")

            if not name or not name.strip():
                feature["properties"]["image"] = None
                unmatched.append("[unnamed feature]")
                continue
            
            norm_name = self.normalize(name)
            matched_key, score = self.find_best_match(norm_name, list(image_keys.keys()))


            if matched_key:
                feature["properties"]["image"] = os.path.join(
                    self.image_folder, image_keys[matched_key]
                )
                feature["properties"]["image_match_score"] = round(score, 2)

            else:
                feature["properties"]["image"] = None
                feature["properties"]["images_match_score"] = 0
                unmatched.append(name)

        #report results
        total = len(data["features"])
        matched = total -len(unmatched)

        print(f"\n Results: {matched}/{total} features matched")

        if unmatched:
            print("\n No image found for:")
            for u in unmatched:
                print(f"  - {u}")

        else:
            print("All features matched successfully!")   

        return data      

    def save_output(self, data):
        """Save updated GeoJSON"""
        # Make sure output directory exists
        output_dir = os.path.dirname(self.output_geojson)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)  

        with open(self.output_geojson, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n Output saved to {self.output_geojson}")

  
    def run(self):
        """Execute full pipeline"""
        self.validate_inputs()

        data = self.attach_images()
        self.save_output(data)


# ---------------- USER INPUT ---------------- #
if __name__ == "__main__":
    print(" GeoJSON Image Organizer")

    input_geojson = input("Enter path to GeoJSON file: ")
    image_folder = input("Enter path to image folder: ")
    output_geojson = input("Enter output GeoJSON file name: ")

    try :
        organizer = GeoImageOrganizer(input_geojson,image_folder, output_geojson,)
        organizer.run()

    except (FileNotFoundError,ValueError) as e :
        print(f"\n Error: {e}")



