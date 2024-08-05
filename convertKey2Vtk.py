import os
import pandas as pd
import vtk
from scipy.spatial.distance import cdist

def read_key_file(key_file_path):
    data = pd.read_csv(key_file_path, skiprows=6, header=None, sep='\s+', usecols=range(13))
    data.columns = ['X', 'Y', 'Z', 'Scale', 'o11', 'o12', 'o13', 'o21', 'o22', 'o23', 'o31', 'o32', 'o33']
    
    # Check for duplicates in the X, Y, Z columns
    duplicates = data.duplicated(subset=['X', 'Y', 'Z'], keep=False)
    if duplicates.any():
        print("Duplicate positions found:", data[duplicates])

    return data

def check_close_spheres(data, threshold=0.1):  # Threshold defines how close points must be to be considered "close"
    coordinates = data[['X', 'Y', 'Z']]
    distances = cdist(coordinates, coordinates)  # Compute pairwise distance matrix

    # Find pairs where distance is less than the threshold, but not zero (not comparing points with themselves)
    close_pairs = (distances < threshold) & (distances > 0)

    if close_pairs.any():
        print("Close spheres detected.")
        for i in range(len(distances)):
            for j in range(i + 1, len(distances)):
                if close_pairs[i, j]:
                    print(f"Spheres at index {i} and {j} are close ({distances[i, j]} units apart).")

    return close_pairs

def create_vtk_from_data(data, vtk_file_path):
    append_filter = vtk.vtkAppendPolyData()
    colors = vtk.vtkUnsignedCharArray()  # Create an array to store color data
    colors.SetNumberOfComponents(3)  # We will store RGB values
    colors.SetName("Colors")  # Set the name of the color array

    color_palette = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]  # Red, Green, Blue

    num_cells = 0  # Track the number of cells added

    for idx, row in data.iterrows():
        # Create sphere
        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(3 * row['Scale'])
        sphere_source.SetCenter(row['X'], row['Y'], row['Z'])
        sphere_source.SetThetaResolution(30)
        sphere_source.SetPhiResolution(30)
        sphere_source.Update()
        append_filter.AddInputData(sphere_source.GetOutput())

        # Increment cell count and add color for the sphere
        num_cells += sphere_source.GetOutput().GetNumberOfCells()
        sphere_color = [255, 255, 255]  # Assuming white for spheres
        for _ in range(sphere_source.GetOutput().GetNumberOfCells()):
            colors.InsertNextTuple3(*sphere_color)

        for i in range(3):
            # Create arrow
            arrow_source = vtk.vtkArrowSource()
            arrow_source.SetTipLength(0.3)
            arrow_source.SetTipRadius(0.1)

            transform = vtk.vtkTransform()
            transform.Translate(row['X'], row['Y'], row['Z'])
            transform.Scale(50, 50, 50)
            transform.Concatenate(get_orientation_transform(row, i))

            transform_filter = vtk.vtkTransformPolyDataFilter()
            transform_filter.SetTransform(transform)
            transform_filter.SetInputConnection(arrow_source.GetOutputPort())
            transform_filter.Update()

            # Increment cell count and add color for the arrow
            num_cells += transform_filter.GetOutput().GetNumberOfCells()
            color = color_palette[i % 3]
            for _ in range(transform_filter.GetOutput().GetNumberOfCells()):
                colors.InsertNextTuple3(*color)

            append_filter.AddInputData(transform_filter.GetOutput())

    append_filter.Update()

    # Ensure the colors array matches the number of cells
    if colors.GetNumberOfTuples() != num_cells:
        print(f"Warning: Number of colors ({colors.GetNumberOfTuples()}) does not match number of cells ({num_cells}).")

    append_filter.GetOutput().GetCellData().SetScalars(colors)  # Attach color data to cells

    # Change to using vtkXMLPolyDataWriter for .vtp output
    writer = vtk.vtkXMLPolyDataWriter()  # Using XML Writer for better handling
    writer.SetFileName(vtk_file_path.replace('.vtk', '.vtp'))  # Ensure the filename ends with .vtp
    writer.SetInputData(append_filter.GetOutput())
    writer.Write()

def get_orientation_transform(row, index):
    transform = vtk.vtkTransform()
    if index == 0:  # First row
        transform.RotateWXYZ(90, row['o11'], row['o12'], row['o13'])  # Rotate around the first row vector
    elif index == 1:  # Second row
        transform.RotateWXYZ(90, row['o21'], row['o22'], row['o23'])  # Rotate around the second row vector
    elif index == 2:  # Third row
        transform.RotateWXYZ(90, row['o31'], row['o32'], row['o33'])  # Rotate around the third row vector
    return transform

def main():
    key_file_path = os.path.expanduser('~/pathToYourKeyFile.key')  # Path to your .key file
    vtk_file_path = os.path.expanduser('~/pathToVtkFileYouCreate.vtk')  # Output VTK file path
    data = read_key_file(key_file_path)
    create_vtk_from_data(data, vtk_file_path)
    print("VTP file has been created.")

if __name__ == "__main__":
    main()
