import argparse
import hashlib
import json
import pathlib
from datetime import datetime, timezone


def now_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def event_hash(event: dict) -> str:
    payload = dict(event)
    payload.pop("event_hash", None)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Install a minimal third-party RC runtime locally.")
    parser.add_argument("root")
    parser.add_argument("--rc-id", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--surface-id", default="surface_cli_default")
    parser.add_argument("--timestamp")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    ts = args.timestamp or now_z()
    event = {
        "event_id": f"{args.rc_id}_evt_init_0001",
        "timestamp": ts,
        "rc_id": args.rc_id,
        "surface": "installer",
        "event_type": "state_commit",
        "world": "default",
        "summary": "RC runtime initialized",
        "previous_hash": None,
        "state_impact": "Creates local minimal RC runtime.",
        "requires_commit": False,
        "authority": "owner",
        "refs": ["install_rc.py"],
    }
    event["event_hash"] = event_hash(event)
    write_json(root / "00_espina/rc_identity.json", {
        "rc_id": args.rc_id,
        "display_name": args.display_name,
        "instance_type": "third_party_runtime_instance",
        "created_at": ts,
        "memory_boundary": "no_private_aster_memory",
    })
    write_json(root / "00_espina/world_registry.json", {"worlds": [{"world_id": "default", "status": "active"}]})
    write_json(root / "00_espina/surface_registry.json", {
        "surfaces": [
            {"surface_id": args.surface_id, "surface_type": "cli", "permission_level": 1, "can_read_current": True, "can_append_event": True, "can_propose_update": False, "can_commit_state": False, "revoked": False},
            {"surface_id": "owner_runtime", "surface_type": "owner_tool", "permission_level": 4, "can_read_current": True, "can_append_event": True, "can_propose_update": True, "can_commit_state": True, "revoked": False}
        ]
    })
    write_json(root / "00_espina/provider_policy.json", {"default_provider": "not_configured", "byok_required": True})
    write_json(root / "00_espina/cost_policy.json", {"monthly_budget_limit": None, "hard_stop_required": True})
    write_json(root / "00_espina/export_policy.json", {"export_required": True, "deletion_required": True})
    write_json(root / "00_espina/event_signature_policy.json", {"policy_id": f"{args.rc_id}_signature_policy_v0", "algorithm": "ed25519", "private_key_storage": "outside_backend"})
    write_json(root / "01_current/CURRENT_POINTER.json", {
        "rc_id": args.rc_id,
        "backend": "local_folder",
        "current_version": f"{args.rc_id}_current_001",
        "state_path": "01_current/state/CURRENT_STATE.json",
        "continuity_path": "01_current/state/CONTINUITY_STATUS.json",
        "open_loops_path": "01_current/state/OPEN_LOOPS.json",
        "latest_events_path": "01_current/events/2026-08-08.jsonl",
        "accepted_head": event["event_hash"],
        "continuity_status": "CONTINUITY_PARTIAL",
        "updated_at": ts,
    })
    write_json(root / "01_current/state/CURRENT_STATE.json", {"rc_id": args.rc_id, "active_world": "default", "active_surface": args.surface_id, "continuity_status": "CONTINUITY_PARTIAL", "last_significant_update": ts})
    write_json(root / "01_current/state/CONTINUITY_STATUS.json", {"rc_id": args.rc_id, "status": "CONTINUITY_PARTIAL", "reason": "new_runtime_not_remote_verified"})
    write_json(root / "01_current/state/OPEN_LOOPS.json", {"rc_id": args.rc_id, "open_loops": [], "updated_at": ts})
    events = root / "01_current/events/2026-08-08.jsonl"
    events.parent.mkdir(parents=True, exist_ok=True)
    events.write_text(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    write_json(root / "02_activation/activation_package_template.json", {"activation_package_id": f"{args.rc_id}_activation_template", "rc_id": args.rc_id, "status": "template_local", "must_read": ["00_espina/rc_identity.json", "00_espina/surface_registry.json", "01_current/CURRENT_POINTER.json"]})
    report = {"status": "RC_LOCAL_RUNTIME_INSTALLED", "root": str(root), "rc_id": args.rc_id, "accepted_head": event["event_hash"]}
    write_json(root / "03_reports/install_rc_report.json", report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
