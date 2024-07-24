import os
import pandas as pd
import vtk

def read_key_file(key_file_path):
    # Read the file using pandas with regular expression for whitespace
    data = pd.read_csv(key_file_path, skiprows=6, header=None, sep='\s+')
    # Select the first four columns, expected to be X, Y, Z, and Scale
    data = data.iloc[:, :4]
    data.columns = ['X', 'Y', 'Z', 'Scale']
    return data

def create_vtk_from_data(data, vtk_file_path):
    points = vtk.vtkPoints()
    scales = vtk.vtkFloatArray()
    scales.SetName("Scale")  # Set the name of the scalar data

    for idx, row in data.iterrows():
        points.InsertNextPoint(row['X'], row['Y'], row['Z'])
        scales.InsertNextValue(row['Scale'])  # Insert scale data

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.GetPointData().SetScalars(scales)  # Associate scale data with the points

    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(vtk_file_path)
    writer.SetInputData(polydata)
    writer.Write()

def main():
    key_file_path = os.path.expanduser('~/pathToYourKeyFile.key')  # Path to your .key file
    vtk_file_path = os.path.expanduser('~/pathToVtkFileYouCreate.vtk')  # Output VTK file path
    data = read_key_file(key_file_path)
    create_vtk_from_data(data, vtk_file_path)
    print("VTK file has been created.")

if __name__ == "__main__":
    main()
