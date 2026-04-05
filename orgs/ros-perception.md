# ROS Perception

> image_pipeline, vision_opencv, laser_filters — ROS perception packages

- **Domain**: Perception / ROS
- **Website**: https://wiki.ros.org
- **GitHub**: https://github.com/ros-perception
- **Repos (non-fork)**: 32
- **Total Stars**: 5,753

## SLAM / Localization

| Repository | Stars | Language | Activity | Description |
|---|---|---|---|---|
| [slam_gmapping](https://github.com/ros-perception/slam_gmapping) | 729 | C++ | Low | http://www.ros.org/wiki/slam_gmapping |
| [depthimage_to_laserscan](https://github.com/ros-perception/depthimage_to_laserscan) | 295 | C++ | Low | Converts a depth image to a laser scan for use with navigation and localization. |
| [openslam_gmapping](https://github.com/ros-perception/openslam_gmapping) | 233 | C++ | Low | — |
| [slam_karto](https://github.com/ros-perception/slam_karto) | 159 | C++ | Inactive | ROS Wrapper and Node for OpenKarto |
| [sparse_bundle_adjustment](https://github.com/ros-perception/sparse_bundle_adjustment) | 60 | C++ | Inactive | Sparse Bundle Adjustment Library (used by slam_karto) |
| [slam_gmapping_test_data](https://github.com/ros-perception/slam_gmapping_test_data) | 3 | — | Inactive | Repo to contain data (like ROS bags) to use for testing and gmapping |

## Sensor / Driver

| Repository | Stars | Language | Activity | Description |
|---|---|---|---|---|
| [laser_filters](https://github.com/ros-perception/laser_filters) | 221 | C++ | Active | Assorted filters designed to operate on 2D planar laser scanners, which use the  |
| [open_karto](https://github.com/ros-perception/open_karto) | 142 | C++ | Low | Catkinized ROS Package of the OpenKarto Library (LGPL3) |
| [imu_pipeline](https://github.com/ros-perception/imu_pipeline) | 129 | C++ | Moderate | Transforms sensor_msgs/Imu messages into new coordinate frames using tf |
| [image_transport_plugins](https://github.com/ros-perception/image_transport_plugins) | 76 | C++ | Active | A set of plugins for publishing and subscribing to sensor_msgs/Image topics in r |
| [calibration](https://github.com/ros-perception/calibration) | 36 | Python | Low | Provides a toolchain to calibrate sensors and URDF robot models. |
| [radar_msgs](https://github.com/ros-perception/radar_msgs) | 27 | CMake | Inactive | A set of standard messages for RADARs in ROS |
| [camera_pose](https://github.com/ros-perception/camera_pose) | 9 | Python | Inactive | — |
| [laser_proc](https://github.com/ros-perception/laser_proc) | 8 | C++ | Moderate | Converts representations of sensor_msgs/LaserScan and sensor_msgs/MultiEchoLaser |

## Middleware / ROS

| Repository | Stars | Language | Activity | Description |
|---|---|---|---|---|
| [vision_msgs](https://github.com/ros-perception/vision_msgs) | 180 | C++ | Active | Algorithm-agnostic computer vision message types for ROS. |
| [point_cloud_transport](https://github.com/ros-perception/point_cloud_transport) | 103 | C++ | Active | Point Cloud Compression for ROS |
| [image_transport_tutorials](https://github.com/ros-perception/image_transport_tutorials) | 76 | C++ | Active | ROS 2 tutorials for image_transport. |
| [laser_assembler](https://github.com/ros-perception/laser_assembler) | 40 | C++ | Low | Provides nodes to assemble point clouds from either LaserScan or PointCloud mess |
| [pcl_msgs](https://github.com/ros-perception/pcl_msgs) | 11 | CMake | Active | ROS package containing PCL-related messages  |

## Other

| Repository | Stars | Language | Activity | Description |
|---|---|---|---|---|
| [image_pipeline](https://github.com/ros-perception/image_pipeline) | 939 | C++ | Active | An image processing pipeline for ROS. |
| [vision_opencv](https://github.com/ros-perception/vision_opencv) | 654 | C++ | Moderate | — |
| [pointcloud_to_laserscan](https://github.com/ros-perception/pointcloud_to_laserscan) | 573 | C++ | Moderate | Converts a 3D Point Cloud into a 2D laser scan. |
| [perception_pcl](https://github.com/ros-perception/perception_pcl) | 469 | C++ | Active | PCL (Point Cloud Library) ROS interface stack |
| [perception_open3d](https://github.com/ros-perception/perception_open3d) | 170 | C++ | Moderate | Open3D analog to perception_pcl, containing conversion functions from Open3D to/ |
| [laser_geometry](https://github.com/ros-perception/laser_geometry) | 163 | C++ | Active | Provides the LaserProjection class for turning laser scan data into point clouds |
| [image_common](https://github.com/ros-perception/image_common) | 145 | C++ | Active | Common code for working with images in ROS |
| [opencv_apps](https://github.com/ros-perception/opencv_apps) | 73 | C++ | Moderate | http://wiki.ros.org/opencv_apps |
| [pcl_conversions](https://github.com/ros-perception/pcl_conversions) | 10 | C++ | Inactive | [deprecated] pcl_conversions has moved to https://github.com/ros-perception/perc |
| [laser_pipeline](https://github.com/ros-perception/laser_pipeline) | 5 | CMake | Inactive | Meta-package for laser_assembler, laser_filters, and laser_geometry. |
| [megatree](https://github.com/ros-perception/megatree) | 4 | C++ | Inactive | — |

## Language Breakdown

| Language | Repos |
|---|---|
| C++ | 25 |
| CMake | 3 |
| Python | 2 |
| Other | 2 |
