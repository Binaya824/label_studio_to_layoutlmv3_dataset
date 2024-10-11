import os
import json
from uuid import uuid4
from PIL import Image
import pytesseract

# Function to create image URL for Label Studio
def create_image_url(filename):
    return f'http://localhost:8080/{filename}'

# Function to convert OCR bounding box coordinates
def convert_bounding_box(left, top, width, height, image_width, image_height):
    return {
        'x': 100 * left / image_width,
        'y': 100 * top / image_height,
        'width': 100 * width / image_width,
        'height': 100 * height / image_height,
        'rotation': 0
    }

# Function to process images and create JSON for Label Studio
def extracted_tables_to_label_studio_json_file_with_tesseract(images_folder_path, default_label="O"):
    label_studio_task_list = []
    
    for image_filename in os.listdir(images_folder_path):
        if image_filename.endswith('.png'):
            output_json = {}
            annotation_result = []

            print(image_filename)

            output_json['data'] = {"ocr": create_image_url(image_filename)}

            img_path = os.path.join(images_folder_path, image_filename)
            img = Image.open(img_path)
            image_width, image_height = img.size

            # OCR extraction with pytesseract
            tesseract_output = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            all_scores = []

            for i, text in enumerate(tesseract_output['text']):
                if text.strip() != "" and tesseract_output["conf"][i] != "-1":
                    bbox = convert_bounding_box(
                        tesseract_output['left'][i],
                        tesseract_output['top'][i],
                        tesseract_output['width'][i],
                        tesseract_output['height'][i],
                        image_width,
                        image_height
                    )

                    region_id = str(uuid4())[:10]
                    score = int(tesseract_output['conf'][i])
                    
                    bbox_result = {
                        'id': region_id,
                        'from_name': 'bbox',
                        'to_name': 'image',
                        'type': 'rectangle',
                        'value': bbox
                    }
                    
                    transcription_result = {
                        'id': region_id,
                        'from_name': 'transcription',
                        'to_name': 'image',
                        'type': 'textarea',
                        'value': dict(text=[text], **bbox),
                        'score': score
                    }
                    
                    label_result = {
                        'id': region_id,
                        'from_name': 'label',
                        'to_name': 'image',
                        'type': 'labels',
                        'value': dict(labels=[default_label], **bbox)
                    }
                    
                    annotation_result.extend([bbox_result, label_result, transcription_result])
                    all_scores.append(score)

            if annotation_result:
                output_json['predictions'] = [{
                    'result': annotation_result,
                    'score': sum(all_scores) / len(all_scores) if all_scores else 0,
                }]
            else:
                output_json['predictions'] = []

            label_studio_task_list.append(output_json)

    # Save label_studio_task_list as a JSON file to import into Label Studio
    with open('Training_json_tesseract.json', 'w') as f:
        json.dump(label_studio_task_list, f, indent=4)

# Path to the folder containing images
images_folder_path = "./images"

# Run the function
extracted_tables_to_label_studio_json_file_with_tesseract(images_folder_path)
