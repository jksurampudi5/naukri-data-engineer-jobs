import pytest
from pathlib import Path
from src.naukri_de.cli import main


def test_naukri_cli_run():
    sample_path = str(Path(__file__).parent.parent / "data" / "sample" / "fictional_naukri_jobs.json")
    exit_code = main(["--sample", sample_path, "--top", "3", "--report"])
    assert exit_code == 0
