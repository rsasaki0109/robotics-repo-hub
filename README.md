# robotics-repo-hub

A curated catalog of notable repositories from major robotics GitHub organizations.

Each organization page lists top repos by stars with activity status and language breakdown.

---

## Organizations

| Organization | Domain | Repos | Stars | Catalog |
|---|---|---|---|---|
| [Autoware Foundation](https://github.com/autowarefoundation) | Autonomous Driving | 80 | 14,629 | [View](orgs/autowarefoundation.md) |
| [ros2_control](https://github.com/ros-controls) | Control | 29 | 4,750 | [View](orgs/ros-controls.md) |
| [micro-ROS](https://github.com/micro-ROS) | Embedded / Middleware | 30 | 2,858 | [View](orgs/micro-ROS.md) |
| [Open-RMF](https://github.com/open-rmf) | Fleet Management | 70 | 2,108 | [View](orgs/open-rmf.md) |
| [ROBOTIS](https://github.com/ROBOTIS-GIT) | Hardware / Education | 111 | 7,032 | [View](orgs/ROBOTIS-GIT.md) |
| [ANYbotics](https://github.com/ANYbotics) | Legged Robots / Industry | 26 | 6,134 | [View](orgs/ANYbotics.md) |
| [MoveIt](https://github.com/moveit) | Manipulation | 41 | 6,274 | [View](orgs/moveit.md) |
| [ROS 2](https://github.com/ros2) | Middleware | 92 | 14,690 | [View](orgs/ros2.md) |
| [Nav2 (ROS Navigation)](https://github.com/ros-navigation) | Navigation | 10 | 4,748 | [View](orgs/ros-navigation.md) |
| [Point Cloud Library (PCL)](https://github.com/PointCloudLibrary) | Perception / 3D | 9 | 11,387 | [View](orgs/PointCloudLibrary.md) |
| [Drake (Robot Locomotion Group)](https://github.com/RobotLocomotion) | Planning / Simulation | 35 | 6,013 | [View](orgs/RobotLocomotion.md) |
| [Gazebo](https://github.com/gazebosim) | Simulation | 46 | 3,465 | [View](orgs/gazebosim.md) |
| [HKUST Aerial Robotics](https://github.com/HKUST-Aerial-Robotics) | University / Aerial & SLAM | 68 | 33,655 | [View](orgs/HKUST-Aerial-Robotics.md) |
| [Georgia Tech BORG Lab](https://github.com/borglab) | University / Factor Graphs | 16 | 4,242 | [View](orgs/borglab.md) |
| [ETH RSL (Legged Robotics)](https://github.com/leggedrobotics) | University / Legged Robots | 124 | 22,270 | [View](orgs/leggedrobotics.md) |
| [Kenji Koide (AIST / SLAM)](https://github.com/koide3) | University / LiDAR Registration | 61 | 13,184 | [View](orgs/koide3.md) |
| [Giseop Kim (SNU / SLAM)](https://github.com/gisbi-kim) | University / LiDAR SLAM | 80 | 4,836 | [View](orgs/gisbi-kim.md) |
| [Tixiao Shan (LIO-SAM)](https://github.com/TixiaoShan) | University / LiDAR SLAM | 13 | 7,653 | [View](orgs/TixiaoShan.md) |
| [UT Austin ARISE (robosuite)](https://github.com/ARISE-Initiative) | University / Manipulation & Sim | 8 | 3,858 | [View](orgs/ARISE-Initiative.md) |
| [Stanford ASL](https://github.com/StanfordASL) | University / Planning | 123 | 3,114 | [View](orgs/StanfordASL.md) |
| [Univ. Freiburg Robot Learning](https://github.com/robot-learning-freiburg) | University / Robot Learning | 61 | 2,118 | [View](orgs/robot-learning-freiburg.md) |
| [ETH Zurich ASL](https://github.com/ethz-asl) | University / SLAM & Mapping | 226 | 35,620 | [View](orgs/ethz-asl.md) |
| [MIT SPARK Lab](https://github.com/MIT-SPARK) | University / Spatial Perception | 78 | 14,765 | [View](orgs/MIT-SPARK.md) |
| [Univ. Zaragoza SLAM Lab](https://github.com/UZ-SLAMLab) | University / Visual SLAM | 8 | 8,806 | [View](orgs/UZ-SLAMLab.md) |
| [UD RPNG (OpenVINS)](https://github.com/rpng) | University / Visual-Inertial | 41 | 7,155 | [View](orgs/rpng.md) |
| [Foxglove](https://github.com/foxglove) | Visualization / DevTools | 53 | 1,816 | [View](orgs/foxglove.md) |

---

## How to Update

```bash
# Requires: gh CLI (authenticated)
python3 scripts/fetch_and_generate.py
```

## Adding an Organization

Edit the `ORGANIZATIONS` dict in `scripts/fetch_and_generate.py` and re-run.

---

*Last updated: 2026-04-05*
