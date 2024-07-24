from PIL import Image
import numpy as np
import nibabel as nib

def convert_jpg_to_nii(jpg_path, nii_path):
    # Load the JPG image
    with Image.open(jpg_path) as img:
        # Convert the image to grayscale
        img_data = np.array(img.convert('L'))

    # Add a new axis to make it a 3D array if necessary
    if img_data.ndim == 2:
        img_data = img_data[:, :, np.newaxis]

    # Create a NIfTI image;
    affine = np.eye(4)
    nifti_img = nib.Nifti1Image(img_data, affine)

    # Save the NIfTI file
    nib.save(nifti_img, nii_path)
    print(f"Converted {jpg_path} to {nii_path}")

# Directories to process
directories = {
    'y00_nifti/ConvJPG': (1328, 1347),
    'y01_nifti/ConvJPG': (0, 19)
}

base_dir = '~/yourInputFilePath'
output_base_dir = '~/yourOutputFilePath'

# Iterate over directories and file ranges
for dir_key, (start, end) in directories.items():
    input_dir = f"{base_dir}{dir_key}/"
    output_dir = f"{output_base_dir}{dir_key}_nii/"

    # Convert a range of files
    for i in range(start, end + 1):
        jpg_filename = f"concrete_{dir_key.split('_')[0]}_{i:05d}.jpg"
        nii_filename = f"concrete_{dir_key.split('_')[0]}_{i:05d}.nii"

        jpg_path = input_dir + jpg_filename
        nii_path = output_dir + nii_filename

        convert_jpg_to_nii(jpg_path, nii_path)
