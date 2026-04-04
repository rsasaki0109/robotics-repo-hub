#!/usr/bin/env python3
"""
fetch_and_generate.py
Fetch repository metadata from multiple robotics GitHub organizations
and generate per-org Markdown catalogs.

Usage:
    python3 scripts/fetch_and_generate.py [--orgs-dir orgs] [--enrich]

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
    "ANYbotics": {
        "display_name": "ANYbotics",
        "domain": "Legged Robots / Industry",
        "url": "https://www.anybotics.com",
        "description": "ANYmal quadruped — grid_map, elevation_mapping, kindr",
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
}


def fetch_repos(org: str) -> list[dict]:
    """Fetch all repos from a GitHub organization or user via gh CLI."""
    # Try org first, fall back to user
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
    """Generate a Markdown catalog for one organization."""
    # Filter: non-fork, non-archived, has at least 1 star
    notable = [
        r for r in repos
        if not r.get("fork") and not r.get("archived") and r.get("stargazers_count", 0) >= 1
    ]
    notable.sort(key=lambda r: -r.get("stargazers_count", 0))

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

    # Top repos table
    lines.append("## Notable Repositories\n")
    lines.append("| Repository | Stars | Language | Activity | Description |")
    lines.append("|---|---|---|---|---|")

    for r in notable[:50]:
        name = r["name"]
        stars = r.get("stargazers_count", 0)
        lang = r.get("language") or "—"
        activity = activity_badge(r.get("pushed_at", ""))
        desc = (r.get("description") or "—")[:80]
        url = r.get("html_url", "")
        lines.append(f"| [{name}]({url}) | {stars:,} | {lang} | {activity} | {desc} |")

    lines.append("")

    # Stats
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


def generate_readme(org_data: dict[str, dict]) -> str:
    """Generate the top-level README."""
    lines = []
    lines.append("# robotics-repo-hub\n")
    lines.append("A curated catalog of notable repositories from major robotics GitHub organizations.\n")
    lines.append("Each organization page lists top repos by stars with activity status and language breakdown.\n")
    lines.append("---\n")
    lines.append("## Organizations\n")
    lines.append("| Organization | Domain | Repos | Stars | Catalog |")
    lines.append("|---|---|---|---|---|")

    for org_key, info in sorted(ORGANIZATIONS.items(), key=lambda x: x[1]["domain"]):
        data = org_data.get(org_key, {})
        total = data.get("total", 0)
        stars = data.get("stars", 0)
        lines.append(
            f"| [{info['display_name']}](https://github.com/{org_key}) "
            f"| {info['domain']} | {total} | {stars:,} "
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


def main():
    parser = argparse.ArgumentParser(description="Robotics org repo catalog generator")
    parser.add_argument("--orgs-dir", default="orgs")
    args = parser.parse_args()

    orgs_dir = Path(args.orgs_dir)
    orgs_dir.mkdir(parents=True, exist_ok=True)
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    org_data = {}

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

    # Generate README
    readme = generate_readme(org_data)
    Path("README.md").write_text(readme)
    print("Generated README.md", file=sys.stderr)
    print("Done.", file=sys.stderr)


if __name__ == "__main__":
    main()
