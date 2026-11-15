
from pathlib import Path
from PIL import Image, UnidentifiedImageError #pillow
import json
from hashlib  import sha256
import shutil


def open_image(picture):
    try:
        with Image.open(picture) as image:
            width,height=image.size
            return {"width": width, "height": height}
    except UnidentifiedImageError as e:
        return {"error": "UnidentifiedImageError"}
    except FileNotFoundError as e:
        return  {"error": "FileNotFoundError"}


def scan_images(input_dir: Path):
    scanned_images={}
    for file in input_dir.rglob("*"):
        if file.is_file() and file.suffix.lower() in { '.jpg', '.png', '.jpeg'}:
            relative_path = file.relative_to(input_dir).as_posix()
            picture_info=open_image(file)
            picture_info["id"]=sha256(relative_path.encode("utf-8")).hexdigest()
            scanned_images[relative_path]=picture_info

    # with open("report.json", "w", encoding="utf-8") as report:  #saving report json
    #    json.dump(scanned_images, report, indent=2)

    return scanned_images

def export_images(input_dir: Path, output_dir: Path, report):
    for rel_path, info in report.items():
        if "error" in report:
            continue
        else:
            source = input_dir / rel_path
            destination = output_dir / rel_path
            if destination.exists():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

def main():

    working_directory = Path("samples")
    export_directory = Path("export")

    scanned=scan_images(working_directory)
    with open("report.json", "w", encoding="utf-8") as report:
        json.dump(scanned, report, indent=2)

    export_images(working_directory, export_directory, json.load(open("report.json", "r", encoding="utf-8")))

if __name__ == '__main__':
    main()
