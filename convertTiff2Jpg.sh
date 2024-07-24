#!/bin/bash

# Define the input and output directories
input_dir=~/pathToYourInputDir
output_dir=~/pathToYourOutputDir
input_dir2=~/pathToYourInputDir2
output_dir2=~/pathToYourOutputDir2

# Iterate over the range of files
for i in $(seq -f "%05g" 0 19); do
    input_file="${input_dir}nameOfTiffFileUntilIdentifier_${i}.tiff"
    output_file="${output_dir}nameOfJPGFileUntilIdentifier_${i}.jpg"
    
    # Convert TIFF to JPG
    convert "$input_file" "$output_file"
    
    # Print status
    echo "Converted $input_file to $output_file"
done
for i in $(seq -f "%05g" 1328 1347); do
    input_file="${input_dir2}nameOfTiffFileUntilIdentifier_${i}.tiff"
    output_file="${output_dir2}nameOfJPGFileUntilIdentifier_${i}.jpg"
    
    # Convert TIFF to JPG
    convert "$input_file" "$output_file"
    
    # Print status
    echo "Converted $input_file to $output_file"
done

