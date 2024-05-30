import os
import laspy
import numpy as np

def convert_csv_to_laz(csv_file, output_dir):
    """
    Function to convert point cloud data from a CSV file to LAZ files for each frame.

    Parameters:
        csv_file (str): Path to the CSV file.
        output_dir (str): Directory to save the generated LAZ files.
    """
    try:
        # Load the csv file
        data = np.loadtxt(csv_file, delimiter=',', skiprows=1)
        
        # Extract the base filename from the csv file path
        base_filename = os.path.splitext(os.path.basename(csv_file))[0]
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get unique frame numbers
        frame_numbers = np.unique(data[:, 0])

        # Iterate over each frame
        for frame_number in frame_numbers:
            # Get points for the current frame
            frame_data = data[data[:, 0] == frame_number]
            xyz = frame_data[:, 2:5]

            # Create LAZ file for the current frame
            output_file = os.path.join(output_dir, f"{base_filename}_frame_{int(frame_number):04d}.laz")
            print(f"Creating LAZ file for frame {int(frame_number)}:", output_file)
            out_laz = laspy.create(file_version='1.2', point_format=3)
            # Set X, Y, Z coordinates
            out_laz.x = xyz[:, 0]
            out_laz.y = xyz[:, 1]
            out_laz.z = xyz[:, 2]
            # Save the LAZ file
            print("Writing LAZ file...")
            out_laz.write(output_file)

        print("All frames processed successfully.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Input directory containing CSV files
    csv_directory = "/Volumes/ExtremeSSD/people_moving_csv"
    # Output directory for LAZ files
    output_dir = "/Volumes/ExtremeSSD/people_moving_laz"

    # Iterate over all CSV files in the directory
    for csv_file in os.listdir(csv_directory):
        if csv_file.endswith(".csv"):
            csv_file_path = os.path.join(csv_directory, csv_file)
            convert_csv_to_laz(csv_file_path, output_dir)