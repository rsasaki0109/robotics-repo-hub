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
| [MoveIt](https://github.com/moveit) | Manipulation | 41 | 6,274 | [View](orgs/moveit.md) |
| [ROS 2](https://github.com/ros2) | Middleware | 92 | 14,690 | [View](orgs/ros2.md) |
| [Nav2 (ROS Navigation)](https://github.com/ros-navigation) | Navigation | 10 | 4,748 | [View](orgs/ros-navigation.md) |
| [Point Cloud Library (PCL)](https://github.com/PointCloudLibrary) | Perception / 3D | 9 | 11,387 | [View](orgs/PointCloudLibrary.md) |
| [Drake (Robot Locomotion Group)](https://github.com/RobotLocomotion) | Planning / Simulation | 35 | 6,013 | [View](orgs/RobotLocomotion.md) |
| [Gazebo](https://github.com/gazebosim) | Simulation | 46 | 3,465 | [View](orgs/gazebosim.md) |
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
