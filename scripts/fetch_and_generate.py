#!/usr/bin/env python3
"""
fetch_and_generate.py
Fetch repository metadata from multiple robotics GitHub organizations
and generate per-org Markdown catalogs + JSON for GitHub Pages.

Usage:
    python3 scripts/fetch_and_generate.py [--orgs-dir orgs]

Requires: gh CLI (authenticated)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Target organizations ──────────────────────────────────────────
ORGANIZATIONS = {
    "autowarefoundation": {
        "display_name": "Autoware Foundation",
        "domain": "Autonomous Driving",
        "url": "https://autoware.org",
        "description": "Open-source autonomous driving software stack",
    },
    "ros2": {
        "display_name": "ROS 2",
        "domain": "Middleware",
        "url": "https://docs.ros.org",
        "description": "Robot Operating System 2 core packages",
    },
    "moveit": {
        "display_name": "MoveIt",
        "domain": "Manipulation",
        "url": "https://moveit.ai",
        "description": "Motion planning framework for robotic arms",
    },
    "ros-navigation": {
        "display_name": "Nav2 (ROS Navigation)",
        "domain": "Navigation",
        "url": "https://nav2.org",
        "description": "ROS 2 navigation stack",
    },
    "ros-controls": {
        "display_name": "ros2_control",
        "domain": "Control",
        "url": "https://control.ros.org",
        "description": "Hardware abstraction and controller framework for ROS 2",
    },
    "gazebosim": {
        "display_name": "Gazebo",
        "domain": "Simulation",
        "url": "https://gazebosim.org",
        "description": "Open-source robotics simulator",
    },
    "open-rmf": {
        "display_name": "Open-RMF",
        "domain": "Fleet Management",
        "url": "https://www.open-rmf.org",
        "description": "Open Robot Management Framework for multi-robot systems",
    },
    "foxglove": {
        "display_name": "Foxglove",
        "domain": "Visualization / DevTools",
        "url": "https://foxglove.dev",
        "description": "Observability and visualization platform for robotics",
    },
    "PointCloudLibrary": {
        "display_name": "Point Cloud Library (PCL)",
        "domain": "Perception / 3D",
        "url": "https://pointclouds.org",
        "description": "Large-scale 2D/3D point cloud processing",
    },
    "RobotLocomotion": {
        "display_name": "Drake (Robot Locomotion Group)",
        "domain": "Planning / Simulation",
        "url": "https://drake.mit.edu",
        "description": "Model-based design and control for robotics",
    },
    "ROBOTIS-GIT": {
        "display_name": "ROBOTIS",
        "domain": "Hardware / Education",
        "url": "https://www.robotis.com",
        "description": "Dynamixel servos, TurtleBot3, OpenManipulator",
    },
    "micro-ROS": {
        "display_name": "micro-ROS",
        "domain": "Embedded / Middleware",
        "url": "https://micro.ros.org",
        "description": "ROS 2 on microcontrollers",
    },
    # ── AI / Embodied AI ─────────────────────────────────────────
    "huggingface": {
        "display_name": "Hugging Face",
        "domain": "AI / Foundation Models",
        "url": "https://huggingface.co",
        "description": "Open-source ML platform — Transformers, Diffusers, LeRobot",
    },
    "google-deepmind": {
        "display_name": "Google DeepMind",
        "domain": "AI / Research",
        "url": "https://deepmind.google",
        "description": "RT-2, PaLM-E, Gemini robotics, AlphaFold",
    },
    "facebookresearch": {
        "display_name": "Meta FAIR",
        "domain": "AI / Research",
        "url": "https://ai.meta.com",
        "description": "PyTorch, Habitat, Detic, SAM, Segment Anything",
    },
    "openai": {
        "display_name": "OpenAI",
        "domain": "AI / Foundation Models",
        "url": "https://openai.com",
        "description": "GPT, CLIP, Whisper, Gym, Safety Gym",
    },
    "NVIDIA-AI-IOT": {
        "display_name": "NVIDIA AI-IOT",
        "domain": "AI / Edge & Robotics",
        "url": "https://developer.nvidia.com",
        "description": "Isaac, Jetson inference, TensorRT demos, edge AI for robotics",
    },
    "Physical-Intelligence": {
        "display_name": "Physical Intelligence (pi)",
        "domain": "AI / Embodied Intelligence",
        "url": "https://www.physicalintelligence.company",
        "description": "pi0 — foundation models for physical intelligence and robot control",
    },
    # ── Industry (additional) ────────────────────────────────────
    "bdaiinstitute": {
        "display_name": "Boston Dynamics AI Institute",
        "domain": "Legged Robots / Industry",
        "url": "https://theaiinstitute.com",
        "description": "Boston Dynamics AI Institute — legged robots, manipulation, AI research",
    },
    "UniversalRobots": {
        "display_name": "Universal Robots",
        "domain": "Manipulation / Industry",
        "url": "https://www.universal-robots.com",
        "description": "Universal Robots — collaborative robot arms, ROS drivers",
    },
    "dji-sdk": {
        "display_name": "DJI SDK",
        "domain": "Aerial / Drones",
        "url": "https://developer.dji.com",
        "description": "DJI — drone SDKs, onboard computing, mobile integration",
    },
    "frankaemika": {
        "display_name": "Franka Emika",
        "domain": "Manipulation / Industry",
        "url": "https://franka.de",
        "description": "Franka Emika — Panda robot arm, libfranka, franka_ros2",
    },
    "IntelRealSense": {
        "display_name": "Intel RealSense",
        "domain": "Sensors / Industry",
        "url": "https://www.intelrealsense.com",
        "description": "Intel RealSense — depth cameras, librealsense SDK, ROS wrappers",
    },
    "stereolabs": {
        "display_name": "StereoLabs",
        "domain": "Sensors / Industry",
        "url": "https://www.stereolabs.com",
        "description": "StereoLabs — ZED stereo cameras, depth sensing, spatial mapping",
    },
    "ANYbotics": {
        "display_name": "ANYbotics",
        "domain": "Legged Robots / Industry",
        "url": "https://www.anybotics.com",
        "description": "ANYmal quadruped — grid_map, elevation_mapping, kindr",
    },
    # ── Universities / Research Labs ──────────────────────────────
    "StanfordASL": {
        "display_name": "Stanford ASL",
        "domain": "University / Planning",
        "url": "https://asl.stanford.edu",
        "description": "Stanford Autonomous Systems Lab — motion planning, decision-making",
    },
    "ethz-asl": {
        "display_name": "ETH Zurich ASL",
        "domain": "University / SLAM & Mapping",
        "url": "https://asl.ethz.ch",
        "description": "ETH Autonomous Systems Lab — SLAM, mapping, aerial robotics",
    },
    "leggedrobotics": {
        "display_name": "ETH RSL (Legged Robotics)",
        "domain": "University / Legged Robots",
        "url": "https://rsl.ethz.ch",
        "description": "ETH Robotic Systems Lab — ANYmal, legged locomotion, elevation mapping",
    },
    "HKUST-Aerial-Robotics": {
        "display_name": "HKUST Aerial Robotics",
        "domain": "University / Aerial & SLAM",
        "url": "https://uav.hkust.edu.hk",
        "description": "HKUST — VINS-Mono/Fusion, FAST-LIO, autonomous UAV",
    },
    "MIT-SPARK": {
        "display_name": "MIT SPARK Lab",
        "domain": "University / Spatial Perception",
        "url": "https://web.mit.edu/sparklab",
        "description": "MIT — Kimera, Hydra, spatial perception and scene understanding",
    },
    "borglab": {
        "display_name": "Georgia Tech BORG Lab",
        "domain": "University / Factor Graphs",
        "url": "https://borg.cc.gatech.edu",
        "description": "Georgia Tech — GTSAM, factor graph optimization",
    },
    "robot-learning-freiburg": {
        "display_name": "Univ. Freiburg Robot Learning",
        "domain": "University / Robot Learning",
        "url": "http://rl.uni-freiburg.de",
        "description": "Freiburg — panoptic segmentation, robot learning, navigation",
    },
    "ARISE-Initiative": {
        "display_name": "UT Austin ARISE (robosuite)",
        "domain": "University / Manipulation & Sim",
        "url": "https://arise-initiative.org",
        "description": "UT Austin — robosuite, robomimic, manipulation benchmarks",
    },
    "gisbi-kim": {
        "display_name": "Giseop Kim (SNU / SLAM)",
        "domain": "University / LiDAR SLAM",
        "url": "https://github.com/gisbi-kim",
        "description": "SC-LIO-SAM, LT-mapper, LiDAR place recognition",
    },
    "TixiaoShan": {
        "display_name": "Tixiao Shan (LIO-SAM)",
        "domain": "University / LiDAR SLAM",
        "url": "https://github.com/TixiaoShan",
        "description": "LIO-SAM, LeGO-LOAM — widely-used LiDAR-inertial SLAM",
    },
    "koide3": {
        "display_name": "Kenji Koide (AIST / SLAM)",
        "domain": "University / LiDAR Registration",
        "url": "https://github.com/koide3",
        "description": "small_gicp, ndt_omp, hdl_graph_slam, GLIM",
    },
    "rpng": {
        "display_name": "UD RPNG (OpenVINS)",
        "domain": "University / Visual-Inertial",
        "url": "https://sites.udel.edu/robot",
        "description": "Univ. Delaware — OpenVINS, visual-inertial navigation",
    },
    "UZ-SLAMLab": {
        "display_name": "Univ. Zaragoza SLAM Lab",
        "domain": "University / Visual SLAM",
        "url": "https://github.com/UZ-SLAMLab",
        "description": "ORB-SLAM3 — state-of-the-art visual/visual-inertial SLAM",
    },
    # ── Individual Developers ─────────────────────────────────────
    "rsasaki0109": {
        "display_name": "Ryohei Sasaki",
        "domain": "Individual / Localization & GNSS",
        "url": "https://github.com/rsasaki0109",
        "description": "eagleye contributor, GNSS/IMU localization, lidar_localization_ros2",
    },
    "facontidavide": {
        "display_name": "Davide Faconti",
        "domain": "Individual / ROS Tools",
        "url": "https://github.com/facontidavide",
        "description": "PlotJuggler, BehaviorTree.CPP — essential ROS dev tools",
    },
    "engcang": {
        "display_name": "Engcang Choi",
        "domain": "Individual / SLAM",
        "url": "https://github.com/engcang",
        "description": "SLAM comparison, LiDAR-visual SLAM integration, ROS tools",
    },
    "MizuhoAOKI": {
        "display_name": "Mizuho Aoki",
        "domain": "Individual / Control & Planning",
        "url": "https://github.com/MizuhoAOKI",
        "description": "Vehicle dynamics, path tracking, MPC, control algorithms",
    },
    "neka-nat": {
        "display_name": "neka-nat",
        "domain": "Individual / 3D Vision",
        "url": "https://github.com/neka-nat",
        "description": "Open3D contributions, cupoch (GPU point cloud), 3D processing",
    },
    "AtsushiSakai": {
        "display_name": "Atsushi Sakai",
        "domain": "Individual / Robotics Education",
        "url": "https://github.com/AtsushiSakai",
        "description": "PythonRobotics — robotics algorithms samples, 20k+ stars",
    },
    "SteveMacenski": {
        "display_name": "Steve Macenski",
        "domain": "Individual / Navigation & SLAM",
        "url": "https://github.com/SteveMacenski",
        "description": "Nav2 lead, slam_toolbox, opennav — ROS 2 navigation ecosystem",
    },
    "matlabbe": {
        "display_name": "Mathieu Labbe",
        "domain": "Individual / Visual SLAM",
        "url": "https://github.com/matlabbe",
        "description": "RTAB-Map — RGB-D/Stereo/LiDAR SLAM with loop closure",
    },
    "raulmur": {
        "display_name": "Raul Mur-Artal",
        "domain": "Individual / Visual SLAM",
        "url": "https://github.com/raulmur",
        "description": "ORB-SLAM, ORB-SLAM2 — seminal visual SLAM systems",
    },
    "gaoxiang12": {
        "display_name": "Gao Xiang",
        "domain": "Individual / SLAM Education",
        "url": "https://github.com/gaoxiang12",
        "description": "serta slambook — Introduction to Visual SLAM, 14 lectures",
    },
    "LimHyungTae": {
        "display_name": "Hyungtae Lim (KAIST)",
        "domain": "Individual / LiDAR Perception",
        "url": "https://github.com/LimHyungTae",
        "description": "Patchwork, ERASOR — ground segmentation & dynamic object removal",
    },
    "wjwwood": {
        "display_name": "William Woodall",
        "domain": "Individual / ROS Core",
        "url": "https://github.com/wjwwood",
        "description": "ROS 2 core maintainer, rclcpp, serial library",
    },
    "clalancette": {
        "display_name": "Chris Lalancette",
        "domain": "Individual / ROS Core",
        "url": "https://github.com/clalancette",
        "description": "ROS 2 core maintainer, launch, image_transport",
    },
    "AlexeyAB": {
        "display_name": "Alexey Bochkovskiy",
        "domain": "Individual / Object Detection",
        "url": "https://github.com/AlexeyAB",
        "description": "darknet/YOLOv4 — real-time object detection",
    },
    "hku-mars": {
        "display_name": "HKU MARS Lab",
        "domain": "University / LiDAR SLAM",
        "url": "https://mars.hku.hk",
        "description": "FAST-LIO, FAST-LIO2, ikd-Tree — state-of-the-art LiDAR-inertial SLAM",
    },
    "url-kaist": {
        "display_name": "KAIST URL Lab",
        "domain": "University / Urban Robotics",
        "url": "https://urobot.kaist.ac.kr",
        "description": "KAIST Urban Robotics Lab — MulRan dataset, radar SLAM",
    },
    "introlab": {
        "display_name": "IntRoLab (Sherbrooke)",
        "domain": "University / Visual SLAM",
        "url": "https://introlab.3it.usherbrooke.ca",
        "description": "RTAB-Map, find-object — visual SLAM and object recognition",
    },
    "ultralytics": {
        "display_name": "Ultralytics",
        "domain": "AI / Object Detection",
        "url": "https://ultralytics.com",
        "description": "YOLOv5, YOLOv8, YOLO11 — state-of-the-art real-time detection",
    },
    "Livox-SDK": {
        "display_name": "Livox SDK",
        "domain": "Sensors / Industry",
        "url": "https://www.livoxtech.com",
        "description": "Livox LiDAR — SDK, ROS drivers, FAST-LIO integration",
    },
}


# ── Repo categorization ──────────────────────────────────────────

def categorize_repo(repo: dict) -> str:
    """Categorize a repo based on name, description, topics, and language."""
    name = (repo.get("name") or "").lower()
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in (repo.get("topics") or [])]
    text = f"{name} {desc} {' '.join(topics)}"

    # SLAM / Localization
    if any(k in text for k in ["slam", "localization", "lidar-inertial", "visual-inertial",
                                 "odometry", "place-recognition", "loop-closure",
                                 "ndt", "icp", "scan-matching", "vins", "orb-slam",
                                 "lio-sam", "lego-loam", "fast-lio", "kiss-icp"]):
        return "SLAM / Localization"

    # Perception / Detection / Segmentation
    if any(k in text for k in ["detection", "segmentation", "yolo", "object-detect",
                                 "lidar-detection", "3d-detection", "point-cloud",
                                 "semantic", "panoptic", "instance-seg", "depth-estimation",
                                 "stereo-vision", "optical-flow", "tracker", "tracking"]):
        return "Perception"

    # Planning / Control
    if any(k in text for k in ["planning", "planner", "trajectory", "motion-planning",
                                 "path-planning", "behavior", "mpc", "control",
                                 "controller", "pid", "reinforcement-learning"]):
        if any(k in text for k in ["reinforcement", "rl", "imitation", "policy"]):
            return "Learning / RL"
        return "Planning / Control"

    # Mapping / 3D
    if any(k in text for k in ["mapping", "map", "elevation", "grid-map",
                                 "point-cloud", "pcd", "mesh", "3d-reconstruction",
                                 "voxel", "occupancy", "lanelet"]):
        return "Mapping / 3D"

    # Simulation
    if any(k in text for k in ["simulator", "simulation", "sim", "gazebo", "isaac",
                                 "unity", "unreal", "gym", "environment", "benchmark"]):
        return "Simulation"

    # Navigation
    if any(k in text for k in ["navigation", "nav2", "costmap", "obstacle-avoidance",
                                 "global-planner", "local-planner"]):
        return "Navigation"

    # Manipulation
    if any(k in text for k in ["manipulation", "grasp", "pick-and-place", "robot-arm",
                                 "moveit", "inverse-kinematics", "franka", "panda"]):
        return "Manipulation"

    # Sensor / Driver
    if any(k in text for k in ["driver", "lidar", "camera", "imu", "gnss", "gps",
                                 "sensor", "realsense", "velodyne", "hesai", "ouster",
                                 "radar", "zed", "v4l2", "usb-cam"]):
        return "Sensor / Driver"

    # ML / AI / Foundation Model
    if any(k in text for k in ["transformer", "diffusion", "foundation-model", "llm",
                                 "language-model", "vision-language", "neural-network",
                                 "deep-learning", "machine-learning", "pytorch", "tensorflow",
                                 "training", "inference", "model", "bert", "gpt", "clip",
                                 "sam", "segment-anything"]):
        return "ML / AI"

    # Learning / RL / Imitation
    if any(k in text for k in ["reinforcement", "rl", "imitation", "policy",
                                 "robot-learning", "reward", "demonstration"]):
        return "Learning / RL"

    # Middleware / Communication
    if any(k in text for k in ["ros2", "ros1", "middleware", "dds", "message",
                                 "communication", "transport", "rclcpp", "rclpy",
                                 "micro-ros", "microros"]):
        return "Middleware / ROS"

    # Tools / Utilities
    if any(k in text for k in ["tool", "util", "debug", "visualization", "rviz",
                                 "foxglove", "rosbag", "calibration", "logger",
                                 "converter", "dataset"]):
        return "Tools / Utilities"

    # Documentation
    if any(k in text for k in ["doc", "documentation", "tutorial", "example", "demo"]):
        return "Docs / Examples"

    return "Other"


CATEGORY_ORDER = [
    "SLAM / Localization",
    "Perception",
    "Planning / Control",
    "Navigation",
    "Manipulation",
    "Mapping / 3D",
    "Sensor / Driver",
    "Simulation",
    "ML / AI",
    "Learning / RL",
    "Middleware / ROS",
    "Tools / Utilities",
    "Docs / Examples",
    "Other",
]


def fetch_repos(org: str) -> list[dict]:
    """Fetch all repos from a GitHub organization or user via gh CLI."""
    for endpoint in [f"/orgs/{org}/repos", f"/users/{org}/repos"]:
        try:
            result = subprocess.run(
                [
                    "gh", "api", endpoint,
                    "--paginate",
                    "--jq",
                    '.[] | {name,description,language,stargazers_count,forks_count,'
                    'open_issues_count,topics,fork,archived,pushed_at,updated_at,html_url,'
                    'license: .license.spdx_id}',
                ],
                capture_output=True, text=True, check=True
            )
            lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
            if lines:
                return [json.loads(l) for l in lines]
        except subprocess.CalledProcessError:
            continue
    print(f"  Warning: failed to fetch {org}", file=sys.stderr)
    return []


def activity_badge(pushed_at: str) -> str:
    """Return an activity indicator based on last push date."""
    if not pushed_at:
        return "?"
    try:
        dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - dt).days
        if days < 90:
            return "Active"
        if days < 365:
            return "Moderate"
        if days < 730:
            return "Low"
        return "Inactive"
    except Exception:
        return "?"


def generate_org_md(org_key: str, org_info: dict, repos: list[dict]) -> str:
    """Generate a Markdown catalog for one organization, grouped by category."""
    notable = [
        r for r in repos
        if not r.get("fork") and not r.get("archived") and r.get("stargazers_count", 0) >= 1
    ]

    # Assign categories
    for r in notable:
        r["_category"] = categorize_repo(r)

    lines = []
    lines.append(f"# {org_info['display_name']}\n")
    lines.append(f"> {org_info['description']}\n")
    lines.append(f"- **Domain**: {org_info['domain']}")
    lines.append(f"- **Website**: {org_info['url']}")
    lines.append(f"- **GitHub**: https://github.com/{org_key}")
    total = len([r for r in repos if not r.get("fork") and not r.get("archived")])
    total_stars = sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork"))
    lines.append(f"- **Repos (non-fork)**: {total}")
    lines.append(f"- **Total Stars**: {total_stars:,}")
    lines.append("")

    # Group by category
    by_cat: dict[str, list[dict]] = {}
    for r in notable:
        by_cat.setdefault(r["_category"], []).append(r)

    for cat in CATEGORY_ORDER:
        cat_repos = by_cat.get(cat, [])
        if not cat_repos:
            continue
        cat_repos.sort(key=lambda r: -r.get("stargazers_count", 0))

        lines.append(f"## {cat}\n")
        lines.append("| Repository | Stars | Language | Activity | Description |")
        lines.append("|---|---|---|---|---|")

        for r in cat_repos[:30]:
            name = r["name"]
            stars = r.get("stargazers_count", 0)
            lang = r.get("language") or "—"
            activity = activity_badge(r.get("pushed_at", ""))
            desc = (r.get("description") or "—")[:80]
            url = r.get("html_url", "")
            lines.append(f"| [{name}]({url}) | {stars:,} | {lang} | {activity} | {desc} |")

        lines.append("")

    # Language breakdown
    langs = {}
    for r in repos:
        if not r.get("fork") and not r.get("archived"):
            lang = r.get("language") or "Other"
            langs[lang] = langs.get(lang, 0) + 1
    top_langs = sorted(langs.items(), key=lambda x: -x[1])[:5]
    lines.append("## Language Breakdown\n")
    lines.append("| Language | Repos |")
    lines.append("|---|---|")
    for lang, count in top_langs:
        lines.append(f"| {lang} | {count} |")
    lines.append("")

    return "\n".join(lines)


def _section_key(domain: str) -> str:
    """Map domain to a section heading."""
    if domain.startswith("University /"):
        return "University / Research Labs"
    if domain.startswith("AI /"):
        return "AI / Embodied AI"
    if domain.startswith("Individual /"):
        return "Individual Developers"
    return "Industry / OSS Projects"


def generate_readme(org_data: dict[str, dict]) -> str:
    """Generate the top-level README."""
    lines = []
    lines.append("# robotics-repo-hub\n")
    lines.append("A curated catalog of notable repositories from major robotics GitHub organizations.\n")
    lines.append("Each organization page lists top repos by stars with activity status and language breakdown.\n")
    lines.append("**[Search all repos](https://rsasaki0109.github.io/robotics-repo-hub/)** | ")
    lines.append("[Browse by org](#organizations)\n")
    lines.append("---\n")

    # Group by section
    sections: dict[str, list[tuple[str, dict]]] = {}
    for org_key, info in ORGANIZATIONS.items():
        sec = _section_key(info["domain"])
        sections.setdefault(sec, []).append((org_key, info))

    section_order = ["Industry / OSS Projects", "AI / Embodied AI", "University / Research Labs", "Individual Developers"]

    for section in section_order:
        orgs = sections.get(section, [])
        if not orgs:
            continue
        lines.append(f"## {section}\n")
        lines.append("| Organization | Domain | Description | Repos | Stars | Catalog |")
        lines.append("|---|---|---|---|---|---|")

        orgs_sorted = sorted(orgs, key=lambda x: -org_data.get(x[0], {}).get("stars", 0))
        for org_key, info in orgs_sorted:
            data = org_data.get(org_key, {})
            total = data.get("total", 0)
            stars = data.get("stars", 0)
            domain_short = info["domain"]
            for prefix in ("University / ", "AI / ", "Individual / "):
                if domain_short.startswith(prefix):
                    domain_short = domain_short[len(prefix):]
                    break
            desc = info.get("description", "")
            lines.append(
                f"| [{info['display_name']}](https://github.com/{org_key}) "
                f"| {domain_short} | {desc} | {total} | {stars:,} "
                f"| [View](orgs/{org_key}.md) |"
            )

        lines.append("")

    lines.append("---\n")

    lines.append("## How to Update\n")
    lines.append("```bash")
    lines.append("# Requires: gh CLI (authenticated)")
    lines.append("python3 scripts/fetch_and_generate.py")
    lines.append("```\n")

    lines.append("## Adding an Organization\n")
    lines.append("Edit the `ORGANIZATIONS` dict in `scripts/fetch_and_generate.py` and re-run.\n")

    lines.append("---\n")
    lines.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n")

    return "\n".join(lines)


def generate_search_json(all_repos: list[dict]) -> str:
    """Generate a JSON file for the GitHub Pages search frontend."""
    return json.dumps(all_repos, ensure_ascii=False, indent=1)


def main():
    parser = argparse.ArgumentParser(description="Robotics org repo catalog generator")
    parser.add_argument("--orgs-dir", default="orgs")
    args = parser.parse_args()

    orgs_dir = Path(args.orgs_dir)
    orgs_dir.mkdir(parents=True, exist_ok=True)
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    org_data = {}
    all_repos_for_search = []

    for org_key, org_info in ORGANIZATIONS.items():
        print(f"Fetching {org_key} ({org_info['display_name']})...", file=sys.stderr)
        repos = fetch_repos(org_key)
        print(f"  -> {len(repos)} repos", file=sys.stderr)

        # Save raw data
        raw_path = data_dir / f"{org_key}.jsonl"
        with open(raw_path, "w") as f:
            for r in repos:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        # Generate org page
        md = generate_org_md(org_key, org_info, repos)
        (orgs_dir / f"{org_key}.md").write_text(md)
        print(f"  -> Generated {orgs_dir}/{org_key}.md", file=sys.stderr)

        non_fork = [r for r in repos if not r.get("fork") and not r.get("archived")]
        org_data[org_key] = {
            "total": len(non_fork),
            "stars": sum(r.get("stargazers_count", 0) for r in non_fork),
        }

        # Collect for search JSON (non-fork, non-archived, 1+ star)
        for r in non_fork:
            if r.get("stargazers_count", 0) >= 1:
                all_repos_for_search.append({
                    "name": r["name"],
                    "org": org_key,
                    "org_name": org_info["display_name"],
                    "section": _section_key(org_info["domain"]),
                    "category": categorize_repo(r),
                    "description": r.get("description") or "",
                    "language": r.get("language") or "",
                    "stars": r.get("stargazers_count", 0),
                    "forks": r.get("forks_count", 0),
                    "activity": activity_badge(r.get("pushed_at", "")),
                    "pushed_at": (r.get("pushed_at") or "")[:10],
                    "url": r.get("html_url", ""),
                    "topics": r.get("topics") or [],
                })

    # Generate README
    readme = generate_readme(org_data)
    Path("README.md").write_text(readme)
    print("Generated README.md", file=sys.stderr)

    # Generate search JSON
    all_repos_for_search.sort(key=lambda r: -r["stars"])
    (docs_dir / "repos.json").write_text(generate_search_json(all_repos_for_search))
    print(f"Generated docs/repos.json ({len(all_repos_for_search)} repos)", file=sys.stderr)

    print("Done.", file=sys.stderr)


if __name__ == "__main__":
    main()
