"""
CCTV Redirect Service
"""

import json
import logging
import os
import sys

from flask import Flask, request, abort, redirect, Response

CAM_DATA_PATH = os.environ.get("CAM_DATA_PATH", "/data/cameras.json")
CAM_ID_KEY = "CAMERA_ID"
CAM_IP_FIELD = "CAMERA_IP"
CAM_ID_PARAM = "cam_id"


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)
app = Flask(__name__)


def load_data(path):
    with open(path, "r") as fin:
        return json.load(fin)


def get_camera_by_id(key, val):
    # Load on every request so the most recent source file is referenced.
    try:
        data = load_data(CAM_DATA_PATH)
    except FileNotFoundError:
        logger.error("Camera data file not found: %s", CAM_DATA_PATH)
        abort(503, description="Camera data unavailable")
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Failed to load camera data: %s", exc)
        abort(503, description="Camera data unavailable")

    for row in data:
        if str(row.get(key)) == str(val):
            return row
    return None


@app.get("/")
def index():
    return Response("Not found.", status=404, mimetype="text/plain")


@app.get("/camera/<int:camera_id>")
def get_camera(camera_id):
    """Redirect client to camera feed."""

    if not camera_id:
        return Response("No camera specified.", status=400, mimetype="text/plain")

    cam = get_camera_by_id(CAM_ID_KEY, camera_id)
    if cam is None:
        return Response(
            f"Camera ID {camera_id} not found", status=404, mimetype="text/plain"
        )

    ip = cam.get(CAM_IP_FIELD)
    if not ip:
        logger.error("Camera %s has no %s field", camera_id, CAM_IP_FIELD)
        abort(500, description="Camera record is malformed")

    return redirect(f"http://{ip}", code=302)


@app.get("/healthz")
def healthz():
    """Liveness + readiness: confirm the camera data file is loadable."""
    try:
        load_data(CAM_DATA_PATH)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return Response("unhealthy", status=503, mimetype="text/plain")
    return Response("ok", status=200, mimetype="text/plain")


@app.errorhandler(405)
def method_not_allowed(error):
    return Response("Method not allowed.", status=405, mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
