import os
import rosbag
import laspy
import sensor_msgs.point_cloud2 as pc2
import numpy as np
from collections import defaultdict

def get_pointcloud2_topic(bag_file):
    """
    Function to determine the PointCloud2 topic from a given bag file.

    Parameters:
        bag_file (str): Path to the ROS bag file.

    Returns:
        str: Topic name containing PointCloud2 data, or None if not found.
    """
    # Dictionary to store occurrences of topics with PointCloud2 type
    pointcloud2_topics = defaultdict(int)
    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages():
            if msg._type == 'sensor_msgs/PointCloud2':
                pointcloud2_topics[topic] += 1
    
    # Find the topic with the most occurrences
    if pointcloud2_topics:
        max_occurrences_topic = max(pointcloud2_topics, key=pointcloud2_topics.get)
        return max_occurrences_topic
    else:
        return None

def convert_bag_to_laz(bag_file, output_dir):
    """
    Function to convert PointCloud2 data from a ROS bag file to a LAZ file.

    Parameters:
        bag_file (str): Path to the ROS bag file.
        output_dir (str): Directory to save the generated LAZ files.
    """
    try:
        # Determine the PointCloud2 topic
        pointcloud2_topic = get_pointcloud2_topic(bag_file)
        if not pointcloud2_topic:
            print("No Pointcloud2 topic found in the bag file:", bag_file)
            return
        
        # Open the ROS bag file
        print("Opening ROS bag file:", bag_file)
        bag = rosbag.Bag(bag_file, 'r')

        # Get the total number of messages in the bag file
        total_messages = bag.get_message_count(topic_filters=pointcloud2_topic)
        print("Total messages to process:", total_messages)

        # Create empty lists to store X, Y, Z coordinates
        x_list = []
        y_list = []
        z_list = []

        # Initialize a counter for processed messages
        message_count = 0

        # Find the message type and get the fields
        print("Reading messages from topic {}...".format(pointcloud2_topic))
        for _, msg, _ in bag.read_messages(topics=[pointcloud2_topic]):
            # Increment the counter for processed messages
            message_count += 1
            print("Processing message {}/{}...".format(message_count, total_messages))

            # Iterate over the PointCloud2 message and extract XYZ coordinates
            for point in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True):
                x_list.append(point[0])
                y_list.append(point[1])
                z_list.append(point[2])

        # Close the bag file
        bag.close()

        # Extract the base filename from the bag file path
        base_filename = os.path.splitext(os.path.basename(bag_file))[0]

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create LAZ file
        output_file = os.path.join(output_dir, base_filename + ".laz")
        print("Creating LAZ file:", output_file)
        out_laz = laspy.create(file_version='1.2', point_format=3)
        # Set X, Y, Z coordinates
        out_laz.x = np.array(x_list)
        out_laz.y = np.array(y_list)
        out_laz.z = np.array(z_list)
        # Save the LAZ file
        # out_laz.header.offset = [min(out_laz.x), min(out_laz.y), min(out_laz.z)]
        #out_laz.header.scale = [0.01, 0.01, 0.01]  # Scale the coordinates if necessary
        print("Writing LAZ file...")
        out_laz.write(output_file)

        print("LAZ file created successfully.")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Input directory containing ROS bag files
    bag_directory = "path1"
    # Output directory for LAZ files
    output_dir = "path2"

    # Iterate over all bag files in the directory
    for bag_file in os.listdir(bag_directory):
        if bag_file.endswith(".bag"):
            bag_file_path = os.path.join(bag_directory, bag_file)
            convert_bag_to_laz(bag_file_path, output_dir)

