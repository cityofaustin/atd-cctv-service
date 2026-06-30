"""
Knack -> cameras.json fetcher.
Runs on an interval, writes the camera data atomically to a shared volume.
"""

from datetime import datetime, timezone
import json
import logging
import os
import sys

import knackpy

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

CAM_DATA_PATH = os.environ.get("CAM_DATA_PATH", "/data/cameras.json")
FETCH_LOG_PATH = os.environ.get("FETCH_LOG_PATH", "/data/cameras.log")
KNACK_APP_ID = os.environ["KNACK_APP_ID"]
KNACK_API_KEY = os.environ["KNACK_API_KEY"]
KNACK_CONTAINER = os.environ.get("KNACK_CONTAINER", "view_395")


def fetch_cameras():
    logger.info("Instanciating knack app...")
    app = knackpy.App(app_id=KNACK_APP_ID, api_key=KNACK_API_KEY)
    logger.info("Getting camera records...")
    records = app.get(KNACK_CONTAINER)
    return [record.format() for record in records]


def write_atomic(path, data):
    """Ensure we have a clean file for the server to read from"""
    tmp = f"{path}.tmp"
    with open(tmp, "w") as fout:
        fout.write(data)
    os.replace(tmp, path)  # atomic on POSIX


def main():
    try:
        cameras = fetch_cameras()
    except Exception as e:
        logger.exception("Fetch failed")
        logger.exception(e)
        raise e

    now = int(datetime.now(timezone.utc).timestamp())
    write_atomic(CAM_DATA_PATH, json.dumps(cameras))
    write_atomic(FETCH_LOG_PATH, f"{now}\n")
    logger.info(f"Wrote {len(cameras)} cameras to {CAM_DATA_PATH}")
    logger.info(f"Updated fetch log timestamp to {now}")


if __name__ == "__main__":
    main()
