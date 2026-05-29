import argparse
import csv
import os
import sys
from .core import GeoImageOrganizer
import logging
from pathlib import Path
logger = logging.getLogger(__name__)

def build_parser():
    parser = argparse.ArgumentParser(
        prog="geojson-attach",
        description="Attach images to GeoJSON features using fuzzy matching.",
        epilog="Example: geojson-attach --input map.geojson --images ./photos --output result.geojson"
    )
    parser.add_argument("--input", required=True, help="Path to input GeoJSON file")
    parser.add_argument("--images", required=True, help="Path to folder containing images")
    parser.add_argument("--output", required=True, help="Path to output GeoJSON file")
    parser.add_argument("--cutoff", type=float, default=75.0, help="Match sensitivity 0-100 (default: 75.0)")
    parser.add_argument("--report", action="store_true", help="Export unmatched features to CSV")
    return parser


def export_report(data, output_path):
    report_path = str(Path(output_path).with_stem(Path(output_path).stem + "_unmatched").with_suffix(".csv"))
    unmatched = [
        f["properties"].get("name", "[unnamed]")
        for f in data["features"]
        if f["properties"].get("image") is None
    ]
    with open(report_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["feature_name", "status"])
        for name in unmatched:
            writer.writerow([name, "no image found"])
    logger.info("Report saved to %s", report_path)
    return report_path


def main():
    parser = build_parser()
    args = parser.parse_args()

    logger.info("Input:  %s", args.input)
    logger.info("Images: %s", args.images)
    logger.info("Output: %s", args.output)
    logger.info("Cutoff: %s", args.cutoff)

    try:
        organizer = GeoImageOrganizer(
            input_geojson=args.input,
            image_folder=args.images,
            output_geojson=args.output,
            cutoff=args.cutoff
        )
        organizer.validate_inputs()
        data = organizer.attach_images()
        organizer.save_output(data)

        if args.report:
            export_report(data, args.output)

    except (FileNotFoundError, ValueError) as e:
        print(f"\n Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()