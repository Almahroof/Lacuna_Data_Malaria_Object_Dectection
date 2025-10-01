from ultralytics.data import build_yolo_dataset
from ultralytics.data.utils import check_det_dataset
from pathlib import Path
import shutil
import os

def split_dataset(data_root, split_ratio=(0.7, 0.2, 0.1)):
    """Split dataset into train, validation and test sets."""
    # Create directories
    for split in ['train', 'val', 'test']:
        for folder in ['images', 'labels']:
            Path(data_root / folder / split).mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    image_files = list(Path(data_root / 'images').glob('*.*'))
    image_files = [f for f in image_files if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp'}]
    
    # Calculate split sizes
    num_images = len(image_files)
    num_train = int(num_images * split_ratio[0])
    num_val = int(num_images * split_ratio[1])
    
    # Randomly shuffle files
    import random
    random.shuffle(image_files)
    
    # Split files
    train_files = image_files[:num_train]
    val_files = image_files[num_train:num_train + num_val]
    test_files = image_files[num_train + num_val:]
    
    # Move files to respective directories
    for files, split in zip([train_files, val_files, test_files], ['train', 'val', 'test']):
        for img_path in files:
            # Move image
            shutil.move(str(img_path), str(data_root / 'images' / split / img_path.name))
            
            # Move corresponding label if it exists
            label_path = data_root / 'labels' / f"{img_path.stem}.txt"
            if label_path.exists():
                shutil.move(str(label_path), str(data_root / 'labels' / split / f"{img_path.stem}.txt"))

    return {
        'train': len(train_files),
        'val': len(val_files),
        'test': len(test_files)
    }

# Use the function
data_root = Path('/home/wahrwelt/Downloads/Dataset/Lacuna- Malaria Dataset/Thick_Ghana/data')
results = split_dataset(data_root)

print("\nDataset split complete:")
print(f"Train: {results['train']} images")
print(f"Val: {results['val']} images")
print(f"Test: {results['test']} images")