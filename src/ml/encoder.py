from transformers import  CLIPModel, AutoProcessor
from PIL import Image
import torch



model_name="openai/clip-vit-base-patch32"
model=CLIPModel.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained(model_name)

model.eval()

def encode_image(img_path):
    with Image.open(img_path) as img:
        inputs = processor(images=img.convert("RGB"), return_tensors="pt")

    with torch.inference_mode():
        outputs=model.get_image_features(**inputs)

    embedding = outputs.pooler_output
    embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)
    vector = embedding.squeeze(0).numpy()

    return vector

def main():
    vector = encode_image("sample.jpg")
    print(vector[:20])

if __name__ == '__main__':
    main()