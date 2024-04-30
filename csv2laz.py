import os
import laspy
import numpy as np



def convert_csv_to_laz(csv_file, output_dir):
    """
    Function to convert point cloud data from a CSV file to a LAZ file.

    Parameters:
        csv_file (str): Path to the CSV file.
        output_dir (str): Directory to save the generated LAZ files.
    """
    try:
        # Use Numpy LoadTXT to load the csv file
        # Assume that you are loading X, Y, Z only, can load all if wanted
        xyz = np.loadtxt(csv_file_path,delimiter=',',skiprows=1)[:,2:5]
    

        # Extract the base filename from the bag file path
        base_filename = os.path.splitext(os.path.basename(csv_file))[0]
    
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
    # Input directory containing CSV files
    csv_directory = "path1"
    # Output directory for LAZ files
    output_dir = "path2"

    # Iterate over all CSV files in the directory
    for csv_file in os.listdir(csv_directory):
        if csv_file.endswith(".csv"):
            csv_file_path = os.path.join(csv_directory, csv_file)
            convert_csv_to_laz(csv_file_path, output_dir)

