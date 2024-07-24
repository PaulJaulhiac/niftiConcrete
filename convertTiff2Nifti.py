import os
import numpy as np
import nibabel as nib
from PIL import Image

def convert_tiffs_to_nifti(tiff_directory, output_file):
    # List all TIFF files in the directory sorted alphabetically
    tiff_files = sorted([f for f in os.listdir(tiff_directory) if f.endswith('.tiff') or f.endswith('.tif')])
    
    # Load the first image to get dimensions
    example_img = Image.open(os.path.join(tiff_directory, tiff_files[0]))
    example_array = np.array(example_img)
    
    # Create a 3D array to hold all image data
    img_shape = (example_array.shape[0], example_array.shape[1], len(tiff_files))
    img_data = np.zeros(img_shape, dtype=example_array.dtype)
    
    # Load each image and add it to the array
    for i, filename in enumerate(tiff_files):
        img_path = os.path.join(tiff_directory, filename)
        img = Image.open(img_path)
        img_data[:, :, i] = np.array(img)
    
    # Create a NIfTI image (using an identity matrix for the affine)
    affine = np.eye(4)  # Simple identity matrix, you may need to adjust this
    nifti_img = nib.Nifti1Image(img_data, affine)
    
    # Save the NIfTI image
    nib.save(nifti_img, output_file)
    print(f"Saved NIfTI file to {output_file}")

# Usage example
tiff_directory = os.path.expanduser('~/Documents/niftiConcrete/y01')
output_nifti_file = os.path.expanduser('~/Documents/niftiConcrete/y01_nifti')
convert_tiffs_to_nifti(tiff_directory, output_nifti_file)