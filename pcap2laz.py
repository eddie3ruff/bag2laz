import os
from ouster import client, pcap
import laspy
import numpy as np

def convert_pcap_to_laz(pcap_file, json_file, output_dir):
    try:
        # Load metadata
        with open(json_file, 'r') as f:
            metadata = client.SensorInfo(f.read())

        # Set up source and XYZLut
        source = pcap.Pcap(pcap_file, metadata)
        xyzlut = client.XYZLut(metadata)

        # Set up iterator for LidarScans
        scans = iter(client.Scans(source))

        # Determine the output file name and ensure output directory exists
        base_filename = os.path.splitext(os.path.basename(pcap_file))[0]
        output_file = os.path.join(output_dir, base_filename + ".laz")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("Creating LAZ file:", output_file)
        
        # Initialize the LAS file with appropriate configuration
        out_laz = laspy.create(file_version='1.2', point_format=3)
        points = []

        # Process each scan
        for scan in scans:
            xyz = xyzlut(scan.field(client.ChanField.RANGE))
            xyz_destaggered = client.destagger(metadata, xyz)
            k, m, n = np.shape(xyz_destaggered)
            # Flatten and store points
            points.append(xyz_destaggered.reshape((k*m, n)))

        # Concatenate all points from all scans
        all_points = np.concatenate(points, axis=0)

        # Set X, Y, Z coordinates in the LAZ file
        out_laz.x = all_points[:,0]
        out_laz.y = all_points[:,1]
        out_laz.z = all_points[:,2]

        # Set the header offset and possibly scale
        # out_laz.header.offset = [min(out_laz.x), min(out_laz.y), min(out_laz.z)]
        # out_laz.header.scale = [0.01, 0.01, 0.01]  # Uncomment and adjust if scaling is needed

        # Write and save the LAZ file
        print("Writing LAZ file...")
        out_laz.write(output_file)
        print("LAZ file created successfully.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    pcap_directory = "path1"
    output_dir = "path2"
    for pcap_file in os.listdir(pcap_directory):
        if pcap_file.endswith(".pcap"):
            pcap_file_path = os.path.join(pcap_directory, pcap_file)
            json_file_path = os.path.join(pcap_directory, os.path.splitext(pcap_file)[0]+'.json')
            convert_pcap_to_laz(pcap_file_path, json_file_path, output_dir)
