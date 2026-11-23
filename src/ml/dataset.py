from pathlib import Path
from sklearn.linear_model import LogisticRegression
import numpy as np
from encoder import encode_image

import joblib

def train():
    samples_dir = Path(__file__).resolve().parents[0]/"train_samples"

    x=[]
    y=[]


    for game_dir in sorted(samples_dir.iterdir()):
        if not game_dir.is_dir():
            continue

        for image_path in sorted(game_dir.iterdir()):
            if image_path.is_file() and image_path.suffix.lower() in {".jpg", ".png", ".jpeg"}:
                vector = encode_image(image_path)
                x.append(vector)
                y.append(game_dir.name)

    x = np.stack(x)
    y = np.stack(y)

    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(x,y)

    model_path = Path(__file__).resolve().parent/"classifier.joblib"
    joblib.dump(classifier,model_path)
    print("Classificator saved", model_path)

    print(classifier.classes_)

    print(x.shape)
    print(y.shape)
    print(y)

if __name__ == '__main__':
    train()


