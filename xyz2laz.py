import os
import laspy
import numpy as np

def convert_xyz_to_laz(xyz_file, output_dir):
    """
    Function to convert point cloud data from a XYZ file to a LAZ file.

    Parameters:
        xyz_file (str): Path to the XYZ file.
        output_dir (str): Directory to save the generated LAZ files.
    """
    try:
        # Use Numpy LoadTXT to load the xyz file
        # Assume that you are loading X, Y, Z only, can load all if wanted
        xyz = np.loadtxt(xyz_file_path)
    

        # Extract the base filename from the bag file path
        base_filename = os.path.splitext(os.path.basename(xyz_file))[0]
    
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
        # Create LAZ file
        output_file = os.path.join(output_dir, base_filename + ".laz")
        print("Creating LAZ file:", output_file)
        out_laz = laspy.create(file_version='1.2', point_format=3)
        # Set X, Y, Z coordinates

        out_laz.x = xyz[:,0]
        out_laz.y = xyz[:,1]
        out_laz.z = xyz[:,2]
        # Save the LAZ file
        # out_laz.header.offset = [min(out_laz.x), min(out_laz.y), min(out_laz.z)]
        #out_laz.header.scale = [0.01, 0.01, 0.01]  # Scale the coordinates if necessary
        print("Writing LAZ file...")
        out_laz.write(output_file)
    
        print("LAZ file created successfully.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Input directory containing xyz files
    xyz_directory = "path1"
    # Output directory for LAZ files
    output_dir = "path2"

    # Iterate over all xyz files in the directory
    for xyz_file in os.listdir(xyz_directory):
        if xyz_file.endswith(".xyz"):
            xyz_file_path = os.path.join(xyz_directory, xyz_file)
            convert_xyz_to_laz(xyz_file_path, output_dir)

