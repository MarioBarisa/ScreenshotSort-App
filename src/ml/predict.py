from pathlib import Path
import joblib
from encoder import encode_image

def main():
    directory = Path(__file__).resolve().parent
    classifier = joblib.load(directory/"classifier.joblib")
    test_dir = directory / "test_samples_extra"

    for image_path in sorted(test_dir.iterdir()):
        if not image_path.is_file() or image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue

        vector=encode_image(image_path)
        prediction =  classifier.predict([vector])[0]
        print(f"{image_path.name}: {prediction}")

if __name__ == '__main__':
    main()

