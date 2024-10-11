from pdf2image import convert_from_path
import os

def extract_images_from_pdf(pdf_path, output_dir, start_page_num):
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path)

        # Save each image
        for i, image in enumerate(images, start=start_page_num):
            image_file = os.path.join(output_dir, f"page_{i}.png")
            image.save(image_file, "PNG")
            print(f"Page {i} saved as {image_file}")
        return start_page_num + len(images)  # Return the next starting page number
    except Exception as e:
        print(f"Error extracting images from {pdf_path}: {e}")
        return start_page_num  # In case of error, do not increment the starting page number

def convert_all_pdfs_in_folder(pdf_folder, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_page_num = 1  # Initialize starting page number

    # Loop through all files in the pdf_folder
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            start_page_num = extract_images_from_pdf(pdf_path, output_dir, start_page_num)

# Usage example:
pdf_folder_path = "./pdfs_for_training"
output_directory = "./images1"

convert_all_pdfs_in_folder(pdf_folder_path, output_directory)
