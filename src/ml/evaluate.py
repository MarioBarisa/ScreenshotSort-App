from pathlib import Path
import joblib
from encoder import encode_image

labels = {
    "cyberpunk-2077": "cyberpunk",
    "genshin-impact": "genshin",
    "gta4": "gta",
    "kena-bridge-of-spirits":"kena",
    "pokemon-legends-za": "pokemon",
    "the-last-of-us-part-one": "tlou",
    "zelda-botw": "zelda",
}

def main():
    directory = Path(__file__).resolve().parent
    classifier = joblib.load(directory/"classifier.joblib")
    total_correct=0
    total=0

    for folder_name, expected in labels.items():
        folder = directory/"eval_samples"/folder_name
        correct=0
        count=0

        for image_path in sorted(folder.iterdir()):
            if not image_path.is_file() or image_path.suffix.lower() not in {".jpg", ".png", ".jpeg"}:
                continue

            prediction = classifier.predict([encode_image(image_path)])[0]
            count+=1

            if prediction == expected:
                correct += 1
            else:
                print(f"{image_path.name}: expected {expected}, predicted {prediction}")

        print(f"{expected}: {correct}/{count}")
        total_correct += correct
        total += count

    if total_correct!=total:
        print(f"Accuracy: {total_correct}/{total} ({total_correct / total:.1%})")
    else:
        print("*"*4," Perfectly trained! :) ", "*"*4)

if __name__ == '__main__':
    main()