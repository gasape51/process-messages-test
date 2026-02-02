import subprocess
import os
import shutil

def clear_output_dir(directory="output"):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def test_F01_nominal_execution():
    clear_output_dir("output")
    result = subprocess.run(
        ["./process_messages", "./data/messages.csv", "./data/contacts.csv", "output"],
        capture_output=True
    )

    assert result.returncode == 0
    assert os.path.isdir("output")
    assert len(os.listdir("output")) > 0
    for filename in os.listdir("output"):
        assert filename.endswith(".json")
