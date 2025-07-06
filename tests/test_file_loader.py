import os
import pytest
from orchestrator.file_loader import load_yaml, load_csv

def test_load_yaml():
    sample_yaml = """
    - ACTION: ping_test
      SOURCE: 10.0.0.1
      DESTINATION: 8.8.8.8
    """
    path = "tests/sample.yaml"
    with open(path, "w") as f:
        f.write(sample_yaml)

    tasks = load_yaml(path)
    assert len(tasks) == 1
    assert "csv_data" in tasks[0]
    assert "ACTION" in tasks[0]["csv_data"]

    os.remove(path)

def test_load_csv():
    sample_csv = "ACTION,SOURCE,DESTINATION\nping_test,10.0.0.1,8.8.8.8"
    path = "tests/sample.csv"
    with open(path, "w") as f:
        f.write(sample_csv)

    tasks = load_csv(path)
    assert len(tasks) == 1
    assert "ping_test" in tasks[0]["csv_data"]

    os.remove(path)
