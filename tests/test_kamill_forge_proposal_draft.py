import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "kamill_forge_proposal_draft.py"
FIXTURES = REPO / "tests" / "fixtures" / "kamill_forge_watchdog"


def run_draft(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def test_stdout_only_draft_has_staged_pending_boundaries(tmp_path: Path) -> None:
    out_path = tmp_path / "proposal.md"

    result = run_draft(
        "--input",
        str(FIXTURES / "above_threshold_anchored.json"),
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert not out_path.exists()
    assert "Status: staged-draft" in result.stdout
    assert "Decision: pending" in result.stdout
    assert "Implemented: no" in result.stdout
    assert "Verified: no" in result.stdout
    assert "Log updated: no" in result.stdout
    assert "does not approve" in result.stdout
    assert "/Users/qnb/dev/templates/hermes-core" in result.stdout


def test_explicit_out_writes_draft_to_temp_path(tmp_path: Path) -> None:
    out_path = tmp_path / "proposal.md"

    result = run_draft(
        "--input",
        str(FIXTURES / "above_threshold_anchored.json"),
        "--out",
        str(out_path),
    )

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout.strip() == str(out_path)
    draft = out_path.read_text()
    assert "Status: staged-draft" in draft
    assert "Decision: pending" in draft
    assert "Approved scope, if any: none" in draft


def test_unanchored_discord_draft_keeps_repo_path_null() -> None:
    result = run_draft(
        "--input",
        str(FIXTURES / "above_threshold_unanchored_discord.json"),
    )

    assert result.returncode == 0
    assert "Anchor status: global-unanchored" in result.stdout
    assert "Target repo/path: null" in result.stdout
    assert "retarget source pending user decision" in result.stdout


def test_malformed_input_fails_closed_without_output_file(tmp_path: Path) -> None:
    out_path = tmp_path / "proposal.md"

    result = run_draft(
        "--input",
        str(FIXTURES / "malformed.json"),
        "--out",
        str(out_path),
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert "missing required fields" in result.stderr
    assert not out_path.exists()


def test_output_path_is_restricted_outside_dry_run_or_temp_paths() -> None:
    result = run_draft(
        "--input",
        str(FIXTURES / "above_threshold_anchored.json"),
        "--out",
        str(REPO / "logs" / "proposal.md"),
    )

    assert result.returncode == 2
    assert "logs/kamill-forge/dry-runs/staged-proposals" in result.stderr


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
