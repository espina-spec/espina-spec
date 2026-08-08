import argparse
import json
import pathlib
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal surface CLI wrapper for RC runtime.")
    parser.add_argument("--connector", required=True)
    parser.add_argument("--activation", required=True)
    parser.add_argument("--surface", required=True)
    parser.add_argument("--mode", choices=["read-current", "append-event"], required=True)
    parser.add_argument("--event-id")
    parser.add_argument("--event-type", default="open_loop")
    parser.add_argument("--world", default="default")
    parser.add_argument("--summary", default="")
    parser.add_argument("--state-impact", default="")
    parser.add_argument("--authority", default="surface")
    parser.add_argument("--report")
    args = parser.parse_args()
    cmd = [
        sys.executable,
        str(pathlib.Path(args.connector).resolve()),
        "--activation",
        str(pathlib.Path(args.activation).resolve()),
        "--mode",
        args.mode,
        "--surface",
        args.surface,
    ]
    if args.mode == "append-event":
        cmd += [
            "--event-id", args.event_id,
            "--event-type", args.event_type,
            "--world", args.world,
            "--summary", args.summary,
            "--state-impact", args.state_impact,
            "--authority", args.authority,
        ]
    if args.report:
        cmd += ["--report", args.report]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        report = {"status": "SURFACE_CLI_BLOCKED_OR_FAILED", "returncode": result.returncode, "stderr": result.stderr.strip()}
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
