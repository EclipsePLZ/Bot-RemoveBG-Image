from auth_data import token
from rembg import remove
from PIL import Image
from pathlib import Path

def remove_bg():
    list_of_extensions = ['*.png', '*.jpg', '*.jpeg']
    all_files = []
    
    for ext in list_of_extensions:
        all_files.extend(Path('./Images').glob(ext))
    
    for index, item in enumerate(all_files):
        input_path = Path(item)
        file_name = input_path.stem
        
        output_path = f'./out_Images/{file_name}_output.png'
        
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        
        print(f'Completed: {index + 1}/{len(all_files)}')


def main():
    remove_bg()


if __name__ == '__main__':
    main()