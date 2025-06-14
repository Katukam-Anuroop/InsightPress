import subprocess
from pathlib import Path


def test_cli_invalid_path():
    result = subprocess.run(
        ["insightpress", "run", "nofile.csv"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 1


def test_cli_happy_path(tmp_path: Path):
    csv_file = tmp_path / "input.csv"
    csv_file.write_text("a,b\n1,2\n")

    result = subprocess.run(
        ["insightpress", "run", str(csv_file)],
        cwd=tmp_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0
    assert (tmp_path / "report.pdf").exists()
