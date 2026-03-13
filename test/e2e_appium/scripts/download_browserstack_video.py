#!/usr/bin/env python3
"""
Download a BrowserStack App Automate session video by session ID.

Fetches session metadata via the REST API, then downloads the video recording.

Usage:
    python scripts/download_browserstack_video.py --session-id <SESSION_ID>
    python scripts/download_browserstack_video.py --session-id <SESSION_ID> --output-dir ./videos
    python scripts/download_browserstack_video.py --session-id <SESSION_ID> --output ./my_video.mp4
    python scripts/download_browserstack_video.py --session-id <SESSION_ID> --info-only

Credentials are read from BROWSERSTACK_USERNAME / BROWSERSTACK_ACCESS_KEY env vars.
"""

import argparse
import os
import sys
import time
from pathlib import Path

import requests

API_BASE = "https://api-cloud.browserstack.com/app-automate"
SESSION_ENDPOINT = f"{API_BASE}/sessions/{{session_id}}.json"

VIDEO_POLL_INTERVAL_S = 5
VIDEO_POLL_MAX_ATTEMPTS = 24  # ~2 minutes total


def _get_credentials():
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    if not username or not access_key:
        print(
            "Error: BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY "
            "environment variables are required."
        )
        sys.exit(1)
    return username, access_key


def fetch_session_details(session_id: str, auth: tuple) -> dict:
    """Fetch session metadata from BrowserStack App Automate API."""
    url = SESSION_ENDPOINT.format(session_id=session_id)
    response = requests.get(url, auth=auth, timeout=30)
    response.raise_for_status()
    data = response.json()
    # The API wraps session details under an "automation_session" key
    return data.get("automation_session", data)


def print_session_info(session: dict) -> None:
    """Print a human-readable summary of session metadata."""
    fields = [
        ("Name", "name"),
        ("Status", "status"),
        ("Device", "device"),
        ("OS", "os"),
        ("OS Version", "os_version"),
        ("Duration (s)", "duration"),
        ("Build", "build_name"),
        ("Project", "project_name"),
        ("Reason", "reason"),
        ("Public URL", "public_url"),
        ("Video URL", "video_url"),
        ("Logs", "logs"),
    ]
    print("\n  Session details:")
    for label, key in fields:
        value = session.get(key)
        if value is not None and value != "":
            print(f"    {label}: {value}")
    print()


def wait_for_video_url(session_id: str, auth: tuple) -> str:
    """Poll the session endpoint until video_url is available."""
    for attempt in range(1, VIDEO_POLL_MAX_ATTEMPTS + 1):
        session = fetch_session_details(session_id, auth)
        video_url = session.get("video_url")
        if video_url:
            return video_url
        print(
            f"  Video not yet available (attempt {attempt}/{VIDEO_POLL_MAX_ATTEMPTS}), "
            f"retrying in {VIDEO_POLL_INTERVAL_S}s..."
        )
        time.sleep(VIDEO_POLL_INTERVAL_S)

    print("Error: Video URL not available after maximum polling attempts.")
    sys.exit(1)


def download_video(video_url: str, output_path: Path, auth: tuple) -> Path:
    """Stream-download the video file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Downloading video to {output_path} ...")
    response = requests.get(video_url, auth=auth, stream=True, timeout=120)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    downloaded = 0

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                pct = downloaded * 100 // total
                print(f"\r  Progress: {pct}% ({downloaded}/{total} bytes)", end="")

    print(f"\n  Download complete: {output_path} ({downloaded} bytes)")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Download a BrowserStack session video by session ID",
    )
    parser.add_argument(
        "--session-id",
        required=True,
        help="BrowserStack session ID (hashed_id)",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "--output",
        type=Path,
        help="Explicit output file path (e.g. ./my_video.mp4)",
    )
    output_group.add_argument(
        "--output-dir",
        type=Path,
        default=Path("video_recordings"),
        help="Directory to save the video in (default: video_recordings/)",
    )
    parser.add_argument(
        "--info-only",
        action="store_true",
        help="Print session info without downloading the video",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Fail immediately if video_url is not yet available instead of polling",
    )

    args = parser.parse_args()
    auth = _get_credentials()

    print(f"Fetching session details for {args.session_id} ...")
    try:
        session = fetch_session_details(args.session_id, auth)
    except requests.HTTPError as exc:
        print(f"Error: Failed to fetch session details: {exc}")
        sys.exit(1)

    print_session_info(session)

    if args.info_only:
        return

    video_url = session.get("video_url")
    if not video_url:
        if args.no_wait:
            print("Error: video_url is not available and --no-wait was specified.")
            sys.exit(1)
        print("  Video not immediately available, polling...")
        video_url = wait_for_video_url(args.session_id, auth)

    if args.output:
        output_path = args.output
    else:
        output_path = args.output_dir / f"{args.session_id}.mp4"

    try:
        download_video(video_url, output_path, auth)
    except requests.HTTPError as exc:
        print(f"Error: Failed to download video: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
