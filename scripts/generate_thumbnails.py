"""
Generate 160x160 center-cropped JPEG thumbnails from the first frame of each
skin's WebM preview, then write the thumbnail_path into the skin's JSON record.

Run from the repo root:
    python scripts/generate_thumbnails.py

Re-runnable: skips any skin whose thumbnail file already exists on disk.
"""

import json
from pathlib import Path

import cv2

_REPO_ROOT  = Path(__file__).resolve().parent.parent
_JSON_DIR   = _REPO_ROOT / "raw_json"
_THUMB_DIR  = _REPO_ROOT / "application" / "thumbnails"
_THUMB_SIZE = 160


def _extract_first_frame(webm_path: str):
    cap = cv2.VideoCapture(webm_path)
    ok, frame = cap.read()
    cap.release()
    return frame if ok else None


def _center_crop(frame, size: int):
    h, w = frame.shape[:2]
    scale = size / min(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
    x = (new_w - size) // 2
    y = (new_h - size) // 2
    return resized[y:y + size, x:x + size]


def generate_thumbnails():
    _THUMB_DIR.mkdir(parents=True, exist_ok=True)

    json_files = sorted(_JSON_DIR.glob("*.json"))
    total = len(json_files)
    done = skipped = missing = 0

    for i, json_path in enumerate(json_files):
        data = json.loads(json_path.read_text())
        webm = data.get("webm_filepath", "")

        if not webm or not Path(webm).exists():
            missing += 1
            continue

        thumb_name = Path(webm).stem + ".jpg"
        thumb_path = _THUMB_DIR / thumb_name

        if not thumb_path.exists():
            frame = _extract_first_frame(webm)
            if frame is None:
                missing += 1
                continue
            cropped = _center_crop(frame, _THUMB_SIZE)
            cv2.imwrite(str(thumb_path), cropped, [cv2.IMWRITE_JPEG_QUALITY, 85])
            done += 1
        else:
            skipped += 1

        if data.get("thumbnail_path") != str(thumb_path):
            data["thumbnail_path"] = str(thumb_path)
            json_path.write_text(json.dumps(data, indent=4))

        if (i + 1) % 100 == 0 or (i + 1) == total:
            print(f"  {i + 1}/{total}  generated={done}  skipped={skipped}  no-webm={missing}")

    print(f"\nDone. {done} new thumbnails → {_THUMB_DIR}")


if __name__ == "__main__":
    generate_thumbnails()
