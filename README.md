
# bag2laz

## Overview
`bag2laz` is a Python utility designed to convert LiDAR point clouds stored in ROSbag format into LAS or LAZ files. This conversion makes LiDAR data more accessible and viewable across various platforms using standard point cloud processing tools like CloudCompare.

## Features
- **Convert ROSbag to LAS/LAZ:** Seamlessly transform ROSbag files containing `sensor_msgs/PointCloud2` topics into LAS or LAZ files.
- **Cross-Platform Compatibility:** Enables the use of converted files on different operating systems, including macOS and Windows, with appropriate point cloud visualization tools.
- **Support for ROS Noetic:** Specifically tested and supported under ROS Noetic on Ubuntu 20.04.

## Prerequisites
- **ROS Noetic:** Ensure that ROS Noetic is installed and properly set up on your Ubuntu 20.04 system.
- **Python Packages:** The script requires `rosbag`, `laspy`, and `numpy` to be installed. These can be installed via pip:
  ```shell
  pip install laspy numpy
  ```
  Note: `rosbag` is typically installed with ROS Noetic.

## Installation
Clone the repository to your local machine using:
```shell
git clone https://github.com/eddie3ruff/bag2laz.git
```

## Usage
To use `bag2laz`, simply edit the `/path/to/bags/` and `/path/to/converted_bags/` in the script. You can choose LAZ or LAS depending on the file extension setting.

### Example
Assuming your ROSbag files are located in `/home/user/bagfiles` and you want the converted files in `/home/user/converted_files`, you would run:

```shell
python3 bag2laz.py
```

## Output
The script will process each `.bag` file in the specified directory, converting it to a `.laz` file saved in the specified output directory. The conversion status and any errors will be displayed in the terminal.

## Contributing
Contributions to `bag2laz` are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License
[MIT](https://opensource.org/licenses/MIT)
