# README: Data Conversion Tools

## Overview
This suite of scripts facilitates the conversion between several file formats commonly used in imaging and visualization tasks. 
Supported conversions include:

    .key to .vtk for 3D visualization of features extracted from nifti files, via 3D-SIFT program.
    A program adapted from Laurent Chauvin and Matthew Toews work on feature extraction 
    
Their publication: Chauvin, L., Kumar, K., Wachinger, C., Vangel, M., de Guise, J., Desrosiers, C., Wells, W., Toews, M. and Alzheimer’s Disease Neuroimaging Initiative, 2020. 
                  Neuroimage signature from salient keypoints is highly specific to individuals and shared by close relatives. NeuroImage, 204, p.116208.
          https://doi.org/10.1016/j.neuroimage.2019.116208
          (Contact: laurent.chauvin0@gmail.com, matt.toews@gmail.com)

    .tiff to .jpg for standard image format conversion.
    .jpg to .nifti for medical imaging analysis.
    .tiff to .nifti for use in medical imaging environments.

## Requirements

    Python: Python 3.6 or newer.
    Libraries:
        pandas and vtk for .key to .vtk.
        Pillow for image operations.
        nibabel for handling .nifti files.
        Install required libraries using:

        bash cmd:

        pip install pandas vtk Pillow nibabel

## Scripts

    convertKey2Vtk.py: Converts spatial data from .key files into .vtk format.
    convertTiff2Jpg.sh: Converts .tiff images to .jpg format.
    convertJpg2Nifti.py: Converts .jpg images to .nifti format.
    convertTiff2Nifti.py: Converts .tiff images to .nifti format.

## Usage

    Configuration: Edit each script to specify the input and output file paths.
    Execution:
        Run the desired script from the command line:

        bash cmd:

        python [script_name]

## Examples

Convert .key to .vtk:

    # Input: key file containing XYZ and scale, extracted from NIfTI file using 3D-SIFT program. (Cf. 3DSIFT-Rank-Paul-Jaulhiac_CompileFix) 
    # Output: VTK file with points and scale as scalars.

Convert .jpg to .nifti:

    # Input: JPEG image file.
    # Output: NIfTI file suitable for medical imaging software.

Convert .tiff to .jpg:

    # Input: TIFF image file.
    # Output: JPEG image file.

Convert .tiff to .nifti:

    # Input: TIFF image file.
    # Output: NIfTI file for medical imaging purposes.

## Troubleshooting

    Incorrect File Paths: Ensure file paths in the script are correctly configured for your environment.
    Library Issues: Confirm that all dependencies are installed. Reinstall if there are errors.
    Data Format Errors: Make sure input files adhere to expected formats. Modify scripts to accommodate variations if necessary.

## Additional Notes

    Always test scripts with a small set of files before processing large datasets to ensure configurations are correct.
    Review output files to confirm successful conversions, especially when integrating into new workflows.
