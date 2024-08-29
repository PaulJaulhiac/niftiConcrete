import os
import pandas as pd
import vtk
from scipy.spatial.distance import cdist

# Function to read a key file and return the data as a pandas DataFrame
def read_key_file(key_file_path):
    # Read the file, skipping the first 6 rows and reading all 17 columns
    data = pd.read_csv(key_file_path, skiprows=6, header=None, sep='\s+', usecols=range(17))
    # Assign column names, including e1, e2, e3, and InfoFlag as the last four columns
    data.columns = ['X', 'Y', 'Z', 'Scale', 'o11', 'o12', 'o13', 'o21', 'o22', 'o23', 'o31', 'o32', 'o33', 'e1', 'e2', 'e3', 'InfoFlag']

    # Check for duplicate rows based on X, Y, Z columns
    duplicates = data.duplicated(subset=['X', 'Y', 'Z'], keep=False)
    if duplicates.any():
        print("Duplicate positions found:", data[duplicates])

    return data  # Return the processed data

# Function to check if there are any spheres that are too close to each other
def check_close_spheres(data, threshold=0.1):
    coordinates = data[['X', 'Y', 'Z']]  # Extract coordinates
    distances = cdist(coordinates, coordinates)  # Compute distances between all pairs of points

    # Identify pairs of points that are closer than the threshold and are not the same point
    close_pairs = (distances < threshold) & (distances > 0)

    if close_pairs.any():
        print("Close spheres detected.")
        for i in range(len(distances)):
            for j in range(i + 1, len(distances)):
                if close_pairs[i, j]:
                    print(f"Spheres at index {i} and {j} are close ({distances[i, j]} units apart).")

    return close_pairs  # Return the boolean matrix of close pairs

# Function to create a VTK file from the data
def create_vtk_from_data(data, vtk_file_path, output_type='both'):
    append_filter = vtk.vtkAppendPolyData()  # VTK filter to combine multiple data sets
    colors = vtk.vtkUnsignedCharArray()  # Array to store colors
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    # Define a color palette for the arrows
    color_palette = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

    num_cells = 0  # Track the number of cells in the VTK output

    for idx, row in data.iterrows():  # Iterate over each row in the DataFrame
        if output_type in ['both', 'spheres']:
            # Create a sphere for each data point
            sphere_source = vtk.vtkSphereSource()
            sphere_source.SetRadius(row['Scale'])
            sphere_source.SetCenter(row['X'], row['Y'], row['Z'])
            sphere_source.SetThetaResolution(30)
            sphere_source.SetPhiResolution(30)
            sphere_source.Update()
            append_filter.AddInputData(sphere_source.GetOutput())

            num_cells += sphere_source.GetOutput().GetNumberOfCells()
            sphere_color = [255, 255, 255]  # White color for spheres
            for _ in range(sphere_source.GetOutput().GetNumberOfCells()):
                colors.InsertNextTuple3(*sphere_color)

        if output_type in ['both', 'arrows']:
            for i in range(3):  # Create arrows for the orientation vectors
                arrow_source = vtk.vtkArrowSource()
                arrow_source.SetTipLength(0.3)
                arrow_source.SetTipRadius(0.05)

                transform = vtk.vtkTransform()  # Apply transformation to position and orient the arrows
                transform.Translate(row['X'], row['Y'], row['Z'])
                transform.Scale(10, 10, 10)
                transform.Concatenate(get_orientation_transform(row, i))

                transform_filter = vtk.vtkTransformPolyDataFilter()  # Apply the transformation to the arrow
                transform_filter.SetTransform(transform)
                transform_filter.SetInputConnection(arrow_source.GetOutputPort())
                transform_filter.Update()

                num_cells += transform_filter.GetOutput().GetNumberOfCells()
                color = color_palette[i % 3]  # Assign a color from the palette
                for _ in range(transform_filter.GetOutput().GetNumberOfCells()):
                    colors.InsertNextTuple3(*color)

                append_filter.AddInputData(transform_filter.GetOutput())

    append_filter.Update()

    # Check if the number of colors matches the number of cells
    if colors.GetNumberOfTuples() != num_cells:
        print(f"Warning: Number of colors ({colors.GetNumberOfTuples()}) does not match number of cells ({num_cells}).")

    append_filter.GetOutput().GetCellData().SetScalars(colors)  # Assign colors to the cells

    # Write the combined data to a VTK file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(vtk_file_path.replace('.vtk', '.vtp'))
    writer.SetInputData(append_filter.GetOutput())
    writer.Write()

# Helper function to get the transformation matrix based on orientation vectors
def get_orientation_transform(row, index):
    transform = vtk.vtkTransform()
    if index == 0:
        transform.RotateWXYZ(90, row['o11'], row['o12'], row['o13'])  # Rotate based on the first orientation vector
    elif index == 1:
        transform.RotateWXYZ(90, row['o21'], row['o22'], row['o23'])  # Rotate based on the second orientation vector
    elif index == 2:
        transform.RotateWXYZ(90, row['o31'], row['o32'], row['o33'])  # Rotate based on the third orientation vector
    return transform

# New function to create a VTK file for positive and negative features
def create_vtk_for_positive_negative(data, vtk_file_path):
    append_filter = vtk.vtkAppendPolyData()
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    positive_count = 0
    negative_count = 0

    for idx, row in data.iterrows():
        if row['InfoFlag'] == 0:  # Positive feature
            positive_count += 1
            sphere_color = [255, 255, 0]  # Yellow for positive
        elif row['InfoFlag'] == 16:  # Negative feature
            negative_count += 1
            sphere_color = [0, 0, 255]  # Blue for negative
        else:
            continue  # Skip features that are reoriented (InfoFlag != 0 or 16)

        # Create a sphere for the positive or negative feature
        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(row['Scale'])
        sphere_source.SetCenter(row['X'], row['Y'], row['Z'])
        sphere_source.SetThetaResolution(30)
        sphere_source.SetPhiResolution(30)
        sphere_source.Update()

        append_filter.AddInputData(sphere_source.GetOutput())

        for _ in range(sphere_source.GetOutput().GetNumberOfCells()):
            colors.InsertNextTuple3(*sphere_color)

    append_filter.Update()

    # Assign colors to the cells
    append_filter.GetOutput().GetCellData().SetScalars(colors)

    # Write the VTK file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(vtk_file_path.replace('.vtk', '_positive_negative.vtp'))
    writer.SetInputData(append_filter.GetOutput())
    writer.Write()

    # Print the counts of positive and negative features
    print(f"Number of positive features: {positive_count}")
    print(f"Number of negative features: {negative_count}")


# Main function to orchestrate the reading, processing, and writing of VTK files
def main():
    base_path = os.path.expanduser('~/Documents/Molecules')  # Define the base path

    key_file_path = os.path.join(base_path, 'keyFiles/-w', 'Conformer3D_Sucrose.key')  # Path to the key file
    vtk_file_path_base = os.path.join(base_path, 'visualization/-w', 'Conformer3D_Sucrose')  # Base path for the VTK output files

    if os.path.exists(key_file_path):  # Check if the key file exists
        data = read_key_file(key_file_path)  # Read the key file

        # Generate the combined VTP file with both spheres and arrows
        #create_vtk_from_data(data, f"{vtk_file_path_base}_combined.vtp", output_type='both')
        #print(f"Combined VTP file has been created.")

        # Generate the spheres-only VTP file
        create_vtk_from_data(data, f"{vtk_file_path_base}_spheres.vtp", output_type='spheres')
        print(f"Spheres-only VTP file has been created.")

        # Generate the arrows-only VTP file
        create_vtk_from_data(data, f"{vtk_file_path_base}_arrows.vtp", output_type='arrows')
        print(f"Arrows-only VTP file has been created.")

        # Generate the positive and negative spheres VTP file
        create_vtk_for_positive_negative(data, f"{vtk_file_path_base}_positive_negative.vtp")
        print(f"Positive and Negative spheres VTP file has been created.")

if __name__ == "__main__":
    main()  # Run the main function
