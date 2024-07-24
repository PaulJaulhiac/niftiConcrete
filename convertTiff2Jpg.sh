#!/bin/bash

# Define the input and output directories
input_dir=~/Documents/niftiConcrete/y01/
output_dir=~/Documents/niftiConcrete/y01_nifti/
input_dir2=~/Documents/niftiConcrete/y00/
output_dir2=~/Documents/niftiConcrete/y00_nifti/

# Iterate over the range of files
for i in $(seq -f "%05g" 0 19); do
    input_file="${input_dir}20231210_191049_Claudiane_LC3-2_11132023_comp_0_x00y01_${i}.tiff"
    output_file="${output_dir}20231210_191049_Claudiane_LC3-2_11132023_comp_0_x00y01_${i}.jpg"
    
    # Convert TIFF to JPG
    convert "$input_file" "$output_file"
    
    # Print status
    echo "Converted $input_file to $output_file"
done
for i in $(seq -f "%05g" 1328 1347); do
    input_file="${input_dir2}20231210_191049_Claudiane_LC3-2_11132023_comp_0_x00y00_${i}.tiff"
    output_file="${output_dir2}concrete_y00_${i}.jpg"
    
    # Convert TIFF to JPG
    convert "$input_file" "$output_file"
    
    # Print status
    echo "Converted $input_file to $output_file"
done

