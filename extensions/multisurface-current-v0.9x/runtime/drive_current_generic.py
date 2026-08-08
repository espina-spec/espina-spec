import argparse
import hashlib
import json
import os
import pathlib
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


SCOPES = ["https://www.googleapis.com/auth/drive"]


def now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def service():
    token_path = os.environ.get("ASTER_GOOGLE_DRIVE_OAUTH_TOKEN")
    if not token_path or not pathlib.Path(token_path).exists():
        raise RuntimeError("ASTER_GOOGLE_DRIVE_OAUTH_TOKEN missing")
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    return build("drive", "v3", credentials=creds)


def download_text(svc, file_id: str) -> str:
    return svc.files().get_media(fileId=file_id, supportsAllDrives=True).execute().decode("utf-8")


def update_text(svc, file_id: str, text: str, mime: str) -> dict:
    media = MediaInMemoryUpload(text.encode("utf-8"), mimetype=mime, resumable=False)
    return svc.files().update(fileId=file_id, media_body=media, fields="id,name,modifiedTime,webViewLink", supportsAllDrives=True).execute()


def event_hash(event: dict) -> str:
    payload = dict(event)
    payload.pop("event_hash", None)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_activation(path: pathlib.Path) -> dict:
    package = load_json(path)
    required = ["rc_id", "files", "surfaces"]
    missing = [key for key in required if key not in package]
    if missing:
        raise ValueError(f"activation_package_missing:{missing}")
    return package


def surface(package: dict, surface_id: str) -> dict:
    for item in package["surfaces"]:
        if item.get("surface_id") == surface_id:
            if item.get("revoked"):
                raise PermissionError(f"surface_revoked:{surface_id}")
            return item
    raise PermissionError(f"surface_not_declared:{surface_id}")


def require_surface(package: dict, surface_id: str, event_type: str) -> dict:
    item = surface(package, surface_id)
    if not item.get("can_append_event"):
        raise PermissionError(f"surface_cannot_append:{surface_id}")
    if event_type == "state_commit" and not item.get("can_commit_state"):
        raise PermissionError(f"surface_cannot_commit_state:{surface_id}")
    return item


def read_current(args: argparse.Namespace) -> dict:
    package = load_activation(pathlib.Path(args.activation))
    svc = service()
    pointer = json.loads(download_text(svc, package["files"]["01_current/CURRENT_POINTER.json"]["id"]))
    state = json.loads(download_text(svc, package["files"]["01_current/state/CURRENT_STATE.json"]["id"]))
    report = {"status": "GENERIC_CURRENT_READ", "rc_id": pointer.get("rc_id"), "accepted_head": pointer.get("accepted_head"), "active_world": state.get("active_world")}
    if args.report:
        write_json(pathlib.Path(args.report), report)
    return report


def append_event(args: argparse.Namespace) -> dict:
    package = load_activation(pathlib.Path(args.activation))
    require_surface(package, args.surface, args.event_type)
    svc = service()
    pointer_id = package["files"]["01_current/CURRENT_POINTER.json"]["id"]
    events_path = package["latest_events_path"]
    events_id = package["files"][events_path]["id"]
    pointer_before = json.loads(download_text(svc, pointer_id))
    previous_hash = pointer_before.get("accepted_head")
    event = {
        "event_id": args.event_id,
        "timestamp": args.timestamp or now_z(),
        "rc_id": package["rc_id"],
        "surface": args.surface,
        "event_type": args.event_type,
        "world": args.world,
        "summary": args.summary,
        "previous_hash": previous_hash,
        "state_impact": args.state_impact,
        "requires_commit": False,
        "authority": args.authority,
        "refs": args.refs,
    }
    event["event_hash"] = event_hash(event)
    pointer_recheck = json.loads(download_text(svc, pointer_id))
    if pointer_recheck.get("accepted_head") != previous_hash:
        raise RuntimeError("remote_head_changed_before_write")
    events_text = download_text(svc, events_id)
    if events_text and not events_text.endswith("\n"):
        events_text += "\n"
    events_text += json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n"
    pointer_after = dict(pointer_recheck)
    pointer_after["accepted_head"] = event["event_hash"]
    pointer_after["updated_at"] = event["timestamp"]
    pointer_after["last_generic_surface_event_id"] = event["event_id"]
    update_text(svc, events_id, events_text, "application/x-ndjson")
    update_text(svc, pointer_id, json.dumps(pointer_after, indent=2, ensure_ascii=False) + "\n", "application/json")
    reread = json.loads(download_text(svc, pointer_id))
    report = {"status": "GENERIC_APPEND_VERIFIED" if reread.get("accepted_head") == event["event_hash"] else "GENERIC_APPEND_FAILED", "event_id": event["event_id"], "event_hash": event["event_hash"], "previous_hash": previous_hash, "surface": args.surface}
    if args.report:
        write_json(pathlib.Path(args.report), report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Generic Drive CURRENT connector from an activation package.")
    parser.add_argument("--activation", required=True)
    parser.add_argument("--mode", choices=["read-current", "append-event"], required=True)
    parser.add_argument("--surface")
    parser.add_argument("--event-id")
    parser.add_argument("--event-type", default="open_loop")
    parser.add_argument("--world", default="default")
    parser.add_argument("--summary", default="")
    parser.add_argument("--state-impact", default="")
    parser.add_argument("--authority", default="surface")
    parser.add_argument("--refs", action="append", default=[])
    parser.add_argument("--timestamp")
    parser.add_argument("--report")
    args = parser.parse_args()
    report = read_current(args) if args.mode == "read-current" else append_event(args)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not report["status"].endswith("FAILED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
