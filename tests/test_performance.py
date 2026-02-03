import subprocess
import csv
import os
import shutil
import uuid
import time
import pytest

# Helper functions
@pytest.fixture(autouse=True)
def clean_test_artifacts():
    """Helper to clear and recreate output directory before each test"""
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output")

    yield 
    for f in ["./data/test_messages.csv", "./data/test_contacts.csv"]:
        if os.path.exists(f):
            os.remove(f)

def create_test_csv(filename, content):
    """Helper to create test CSV files"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def run_process_messages(messages_file, contacts_file, output_dir="output"):
    """Helper to run the process_messages program and measure execution time"""
    start_time = time.time()
    
    result = subprocess.run(
        ["./process_messages", messages_file, contacts_file, output_dir],
        capture_output=True,
        text=True
    )
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return result, execution_time

def generate_messages_csv(num_messages, num_contacts):
    """Helper to generate a messages CSV file with specified number of messages"""
    lines = ["id,datetime,direction,content,contact\n"]
    
    for i in range(num_messages):
        msg_id = str(uuid.uuid4())
        timestamp = 1009839600 + i
        direction = "originating" if i % 2 == 0 else "destinating"
        content = f"Test message {i}"
        contact_id = 1000 + (i % num_contacts)
        
        lines.append(f"{msg_id},{timestamp},{direction},{content},{contact_id}\n")
    
    return ''.join(lines)

def generate_contacts_csv(num_contacts):
    """Helper to generate a contacts CSV file with specified number of contacts"""
    lines = ["id,name\n"]
    
    for i in range(num_contacts):
        contact_id = 1000 + i
        name = f"Contact {i}"
        lines.append(f"{contact_id},{name}\n")
    
    return ''.join(lines)


# performance tests cases
def test_P01_small_dataset_performance():
    nb_messages = 10
    nb_contacts = 5
    messages_csv = generate_messages_csv(nb_messages, nb_contacts)
    contacts_csv = generate_contacts_csv(nb_contacts)
    
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    
    result, exec_time = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    print(f"Small dataset execution time: {exec_time} seconds")
    assert result.returncode == 0
    assert exec_time < 1 
    assert len(os.listdir("output")) == nb_messages

@pytest.mark.xfail(reason="Bug: binary only creates 10 files max")
def test_P02_medium_dataset_performance():
    nb_messages = 100
    nb_contacts = 20
    messages_csv = generate_messages_csv(nb_messages, nb_contacts)
    contacts_csv = generate_contacts_csv(nb_contacts)
    
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    
    result, exec_time = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    print(f"Medium dataset execution time: {exec_time} seconds")
    assert result.returncode == 0
    assert exec_time < 2
    assert len(os.listdir("output")) == nb_messages


@pytest.mark.xfail(reason="Bug: binary only creates 10 files max")
def test_P03_large_dataset_performance():
    nb_messages = 1000
    nb_contacts = 50
    messages_csv = generate_messages_csv(nb_messages, nb_contacts)
    contacts_csv = generate_contacts_csv(nb_contacts)
    
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    
    result, exec_time = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    print(f"Large dataset execution time: {exec_time} seconds")
    assert result.returncode == 0
    assert exec_time < 5
    assert len(os.listdir("output")) == nb_messages


@pytest.mark.xfail(reason="Bug: binary only creates 10 files max")
def test_P04_extra_large_dataset_performance():
    nb_messages = 5000
    nb_contacts = 100
    messages_csv = generate_messages_csv(nb_messages, nb_contacts)
    contacts_csv = generate_contacts_csv(nb_contacts)
    
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    
    result, exec_time = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    print(f"Extra large dataset execution time: {exec_time} seconds")
    assert result.returncode == 0
    assert len(os.listdir("output")) == nb_messages


@pytest.mark.xfail(reason="Bug: binary only creates 10 files max")
def test_P05_large_contacts_dataset_performance():
    nb_messages = 100
    nb_contacts = 1000
    messages_csv = generate_messages_csv(nb_messages, nb_contacts)
    contacts_csv = generate_contacts_csv(nb_contacts)
    
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    
    result, exec_time = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    print(f"Large contacts dataset execution time: {exec_time} seconds")
    assert result.returncode == 0
    assert len(os.listdir("output")) == nb_messages

@pytest.mark.xfail(reason="Bug: binary only creates 10 files max")
def test_P06_stability_performance():
    nb_messages = 100
    nb_contacts = 1000
    nb_executions = 20

    messages_csv = generate_messages_csv(nb_messages, nb_contacts)
    contacts_csv = generate_contacts_csv(nb_contacts)

    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)

    times = []
    for _ in range(nb_executions):
        if os.path.exists("output"):
            shutil.rmtree("output")
        os.makedirs("output")
        _, exec_time = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
        assert len(os.listdir("output")) == nb_messages
        times.append(exec_time)

    avg = sum(times) / len(times)

    for t in times:
        assert t < avg * 1.5
    print(f"Stability test average execution time: {avg} seconds")
    
