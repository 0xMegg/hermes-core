import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "kamill_forge_ledger.py"
FIXTURES = REPO / "tests" / "fixtures" / "kamill_forge_watchdog"


def run_ledger(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def test_stdout_only_dry_run_emits_record_without_writing_file(tmp_path: Path) -> None:
    ledger_path = tmp_path / "candidate-ledger.jsonl"

    result = run_ledger(
        "--input",
        str(FIXTURES / "above_threshold_anchored.json"),
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert not ledger_path.exists()
    payload = json.loads(result.stdout)
    assert payload["status"] == "dry_run"
    record = payload["records"][0]
    candidate = record["candidate"]
    assert record["ledger_schema"] == "kamill-forge.phase-1c.candidate-ledger.v1"
    assert record["draft_status"] == "none"
    assert candidate["repo_path"] == "/Users/qnb/dev/templates/hermes-core"
    assert candidate["requires_user_approval"] is True
    assert candidate["auto_apply"] is False


def test_explicit_ledger_out_appends_jsonl(tmp_path: Path) -> None:
    ledger_path = tmp_path / "candidate-ledger.jsonl"

    result = run_ledger(
        "--input",
        str(FIXTURES / "above_threshold_anchored.json"),
        "--ledger-out",
        str(ledger_path),
    )

    assert result.returncode == 0
    assert result.stderr == ""
    lines = ledger_path.read_text().splitlines()
    assert len(lines) == 1
    written = json.loads(lines[0])
    stdout_record = json.loads(result.stdout)["records"][0]
    assert written["candidate"] == stdout_record["candidate"]
    assert written["candidate"]["requires_user_approval"] is True
    assert written["candidate"]["auto_apply"] is False


def test_unanchored_discord_candidate_keeps_repo_path_null() -> None:
    result = run_ledger(
        "--input",
        str(FIXTURES / "above_threshold_unanchored_discord.json"),
    )

    assert result.returncode == 0
    candidate = json.loads(result.stdout)["records"][0]["candidate"]
    assert candidate["anchor_status"] == "global-unanchored"
    assert candidate["repo_path"] is None
    assert candidate["requires_user_approval"] is True
    assert candidate["auto_apply"] is False


def test_malformed_input_fails_closed_without_output_file(tmp_path: Path) -> None:
    ledger_path = tmp_path / "candidate-ledger.jsonl"

    result = run_ledger(
        "--input",
        str(FIXTURES / "malformed.json"),
        "--ledger-out",
        str(ledger_path),
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert "missing required fields" in result.stderr
    assert not ledger_path.exists()


def test_output_path_is_restricted_outside_dry_run_or_temp_paths() -> None:
    result = run_ledger(
        "--input",
        str(FIXTURES / "above_threshold_anchored.json"),
        "--ledger-out",
        str(REPO / "logs" / "candidate-ledger.jsonl"),
    )

    assert result.returncode == 2
    assert "logs/kamill-forge/dry-runs" in result.stderr


def test_script_uses_no_network_or_llm_terms() -> None:
    source = SCRIPT.read_text()
    forbidden_terms = [
        "requests",
        "urllib.request",
        "http.client",
        "socket",
        "openai",
        "anthropic",
        "claude",
        "hermes chat",
    ]
    for term in forbidden_terms:
        assert term not in source
