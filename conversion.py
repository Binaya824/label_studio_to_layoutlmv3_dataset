import json
import shutil
import os
from PIL import Image,ImageFile

dir = "invoce_dataset_label_studio"
src_dir = 'images'
unique_labels_set = set()

ImageFile.LOAD_TRUNCATED_IMAGES = True

with open('./label_studio_data.json', 'r') as json_file:
    data = json.load(json_file)


    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(f'{dir}/{dir}.txt', 'w') as text_file, \
         open(f'{dir}/{dir}_box.txt', 'w') as box_text_file, \
         open(f'{dir}/{dir}_image.txt', 'w') as box_text_file, \
         open(f'{dir}/{dir}_labels.txt', 'w') as labels_text_file:
        pass

    for page_data in data:
        for index, transcription in enumerate(page_data["transcription"]):
            if index < len(page_data["label"]):
                current_label = page_data["label"][index]["labels"][0]
            else:
                print(f"Warning: No label for index {index} in page data.")
                continue

            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0
            original_width = 0
            original_height = 0
            image = page_data["ocr"].split('/')[-1]

            print("image =====>>>>>>" , image)


            with open(f'{dir}/{dir}.txt', 'a') as text_file:
                text_file.write(f"{transcription}\t{current_label}\n")

            with open(f'{dir}/{dir}_box.txt', 'a') as box_text_file:
                box = page_data["bbox"]
                x = box[index]["x"]
                y = box[index]["y"]
                width = box[index]["width"]
                height = box[index]["height"]
                original_width = box[index]["original_width"]
                original_height = box[index]["original_height"]

                x1 = int(x * original_width / 100)
                y1 = int(y * original_height / 100)
                x2 = int((x + width) * original_width / 100)
                y2 = int((y + height) * original_height / 100)

                box_text_file.write(f"{transcription}\t{x1} {y1} {x2} {y2}\n")


            if current_label not in unique_labels_set:
                with open(f'{dir}/{dir}_labels.txt', 'a') as labels_text_file:
                    labels_text_file.write(f"{current_label}\n")
                unique_labels_set.add(current_label)


            with open(f'{dir}/{dir}_image.txt' , 'a') as image_text_file:
                image_text_file.write(f"{transcription}\t{x1} {y1} {x2} {y2}\t{original_width} {original_height}\t{image.replace('.png' , '.jpg')}\n")

images = os.listdir(src_dir)

for img in images:
    print("<==>", img)
    if img.endswith('.png'):
        # Get the base name and change the extension to .jpg
        base_name = os.path.splitext(img)[0]
        new_img_name = f"{base_name}.jpg"

        # Open the .png image and convert it to .jpg
        img_path = os.path.join(src_dir, img)
        img_jpg_path = os.path.join(dir, new_img_name)

        try:
            with Image.open(img_path) as im:
                im.convert('RGB').save(img_jpg_path, 'JPEG')
        except OSError as e:
            print(f"Error processing {img}: {e}")


shutil.make_archive(dir ,'zip' , dir)
shutil.rmtree(dir)
