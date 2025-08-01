#!/usr/bin/env python3

import xmltodict
from tifffile import TiffFile
import argparse
import sys

def eer_to_metadata(eer_path) -> dict:
    try:
        with TiffFile(eer_path) as tif:
            tag = tif.pages[0].tags['65001']
            data = tag.value.decode('UTF-8')
    except Exception as e:
        print(f"Error reading EER file: {e}")
        sys.exit(1)

    try:
        parsed = xmltodict.parse(data)
    except Exception as e:
        print(f"Error parsing XML metadata: {e}")
        sys.exit(1)

    metadata = {}
    for item in parsed["metadata"]["item"]:
        key   = item["@name"]
        value = item["#text"]
        metadata[key] = value

        if "@unit" in item:
            metadata[f"{key}.unit"] = item["@unit"]

    return metadata

def main():
    parser = argparse.ArgumentParser(description="Extract and print metadata from an EER file.")
    parser.add_argument("eer_file", help="Path to the .eer file")
    args = parser.parse_args()

    metadata = eer_to_metadata(args.eer_file)

    for key, value in metadata.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()

