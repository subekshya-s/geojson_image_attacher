import os
import pytest
import tempfile
import json
from geojsonfileandimageattacher.core import GeoImageOrganizer


def test_normalize():
    org = GeoImageOrganizer("a.geojson", "images/", "out.geojson")

    assert org.normalize("Kathmandu") == "kathmandu"
    assert org.normalize("New Road") == "newroad"
    assert org.normalize("new-road") == "newroad"
    assert org.normalize("New_Road") == "newroad"
    assert org.normalize("NEW ROAD") == "newroad"
    assert org.normalize("") == ""          

def test_get_image_mapping():
    # Create a real temporary folder with fake image files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create dummy image files
        open(os.path.join(tmpdir, "kathmandu.jpg"), "w").close()
        open(os.path.join(tmpdir, "New Road.jpg"), "w").close()

        org = GeoImageOrganizer("a.geojson", tmpdir, "out.geojson")
        mapping = org.get_image_mapping()

        assert "kathmandu" in mapping         
        assert "newroad" in mapping             
        assert mapping["kathmandu"] == "kathmandu.jpg"  

def test_attach_images_with_match():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a fake image
        open(os.path.join(tmpdir, "kathmandu.jpg"), "w").close()

        # Create a fake GeoJSON file
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Kathmandu"},
                    "geometry": None
                }
            ]
        }

        # Write it to a temp file
        input_path = os.path.join(tmpdir, "input.geojson")
        with open(input_path, "w") as f:
            json.dump(geojson_data, f)

        output_path = os.path.join(tmpdir, "output.geojson")

        org = GeoImageOrganizer(input_path, tmpdir, output_path)
        result = org.attach_images()

        # The feature should now have an image attached
        image_val = result["features"][0]["properties"]["image"]
        assert image_val is not None
        assert "kathmandu.jpg" in image_val

def test_attach_images_no_match():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Image folder has pokhara, but GeoJSON asks for kathmandu
        open(os.path.join(tmpdir, "pokhara.jpg"), "w").close()

        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Kathmandu"},
                    "geometry": None
                }
            ]
        }

        input_path = os.path.join(tmpdir, "input.geojson")
        with open(input_path, "w") as f:
            json.dump(geojson_data, f)

        output_path = os.path.join(tmpdir, "output.geojson")

        org = GeoImageOrganizer(input_path, tmpdir, output_path)
        result = org.attach_images()

        # Should be None since no match found
        image_val = result["features"][0]["properties"]["image"]
        assert image_val is None

def test_save_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.geojson")

        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }

        org = GeoImageOrganizer("a.geojson", tmpdir, output_path)
        org.save_output(geojson_data)

        assert os.path.exists(output_path)

        with open(output_path) as f:
            loaded = json.load(f)
        assert loaded["type"] == "FeatureCollection"

def test_missing_geojson_raises_error():
    org = GeoImageOrganizer("nonexistent.geojson", "images/", "out.geojson")
    with pytest.raises(FileNotFoundError):
        org.validate_inputs()

def test_missing_image_folder_raises_error():
    # Need a real geojson file for this test
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.geojson")
        with open(input_path, "w") as f:
            json.dump({"type": "FeatureCollection", "features": []}, f)

        org = GeoImageOrganizer(input_path, "nonexistent_folder/", "out.geojson")
        with pytest.raises(FileNotFoundError):
            org.validate_inputs()

def test_invalid_json_raises_error():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write a broken JSON file
        input_path = os.path.join(tmpdir, "bad.geojson")
        with open(input_path, "w") as f:
            f.write("this is not json {{{")

        org = GeoImageOrganizer(input_path, tmpdir, "out.geojson")
        with pytest.raises(ValueError):
            org.load_geojson()