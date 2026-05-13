import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "kamill_forge_watchdog.py"
FIXTURES = REPO / "tests" / "fixtures" / "kamill_forge_watchdog"


def run_watchdog(fixture: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(FIXTURES / fixture),
            *args,
        ],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def test_empty_input_is_quiet_day_with_no_output() -> None:
    result = run_watchdog("empty.json")

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_below_threshold_input_is_quiet_day_with_no_output() -> None:
    result = run_watchdog("below_threshold.json", "--min-observations", "3")

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


def test_above_threshold_anchored_candidate_emits_inert_json() -> None:
    result = run_watchdog("above_threshold_anchored.json", "--min-observations", "3")

    assert result.returncode == 0
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["status"] == "candidate_detected"
    assert payload["run_id"] == "above-threshold-anchored-fixture"
    assert len(payload["candidates"]) == 1
    candidate = payload["candidates"][0]
    assert candidate["lane"] == "experience-distillation"
    assert candidate["anchor_status"] == "anchored"
    assert candidate["repo_path"] == "/Users/qnb/dev/templates/hermes-core"
    assert candidate["rule_id"] == "repeated_observation_count"
    assert candidate["proposed_mutation_class"] == "memory_or_skill"
    assert candidate["requires_user_approval"] is True
    assert candidate["auto_apply"] is False


def test_above_threshold_unanchored_discord_candidate_keeps_repo_path_null() -> None:
    result = run_watchdog("above_threshold_unanchored_discord.json", "--min-observations", "3")

    assert result.returncode == 0
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    candidate = payload["candidates"][0]
    assert candidate["anchor_status"] == "global-unanchored"
    assert candidate["repo_path"] is None
    assert candidate["source_type"] == "discord_observation"
    assert candidate["requires_user_approval"] is True
    assert candidate["auto_apply"] is False


def test_malformed_input_fails_safely_without_dumping_environment() -> None:
    result = run_watchdog("malformed.json")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "invalid candidate" in result.stderr
    assert "API_KEY" not in result.stderr
    assert "TOKEN" not in result.stderr


def test_candidate_id_is_deterministic_for_same_input() -> None:
    first = run_watchdog("above_threshold_anchored.json")
    second = run_watchdog("above_threshold_anchored.json")

    first_payload = json.loads(first.stdout)
    second_payload = json.loads(second.stdout)
    assert first_payload["candidates"][0]["id"] == second_payload["candidates"][0]["id"]


def test_script_uses_no_network_or_llm_imports() -> None:
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
