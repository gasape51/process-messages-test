import base64
import subprocess
import os
import shutil
import json
import uuid 
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

def load_json_file(filepath):
    """Helper to load and return the content of a JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_process_messages(messages_file, contacts_file, output_dir="output"):
    """Helper to run the process_messages program"""
    result = subprocess.run(
        ["./process_messages", messages_file, contacts_file, output_dir],
        capture_output=True,
        text=True
    )
    return result

# Test cases
def test_F01_nominal_execution():
    result = run_process_messages("./data/messages.csv", "./data/contacts.csv", "output")    

    assert result.returncode == 0
    assert os.path.isdir("output")
    assert len(os.listdir("output")) > 0
    for filename in os.listdir("output"):
        assert filename.endswith(".json")


def test_F02_file_uniqueness():
    result = run_process_messages("./data/messages.csv", "./data/contacts.csv", "output")

    assert result.returncode == 0

    with open("./data/messages.csv", 'r') as f:
        lines = f.readlines()
        nb_messages = len(lines) - 1  # Exclude header to get number of messages
    assert len(os.listdir("output")) == nb_messages


def test_F03_default_direction_value():
    messages_csv = """id,datetime,direction,content,contact
cd19a0a2-b73c-4ba1-82ae-89d06dc457c5,1770050099,,Test message F03,1001"""
    
    contacts_csv = """id,name
1001,Test Contact"""
    
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")

    assert result.returncode == 0
    
    json_file = "output/cd19a0a2-b73c-4ba1-82ae-89d06dc457c5.json"
    assert os.path.exists(json_file)
    
    data = load_json_file(json_file)

    assert data["direction"] == "originating"



def test_F04_file_naming_convention():
    messages_csv = """id,datetime,direction,content,contact
be5792c2-1c1f-409f-9ac8-27a126efa091,1770050097,originating,Test message F04,1002"""
    
    contacts_csv = """id,name
1002,Another Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")

    assert result.returncode == 0
    
    expected_filename = "be5792c2-1c1f-409f-9ac8-27a126efa091.json"
    assert expected_filename in os.listdir("output")


def test_F05_json_structure_integrity():
    result = run_process_messages("./data/messages.csv", "./data/contacts.csv", "output")

    assert result.returncode == 0   

    required_fields = ["id", "datetime", "direction", "content", "contact"]
    
    json_files = os.listdir("output")
    assert len(json_files) > 0
    
    for json_file in json_files:
        data = load_json_file(f"output/{json_file}")
        
        for field in required_fields:
            assert field in data


def test_F06_id_accuracy():
    result = run_process_messages("./data/messages.csv", "./data/contacts.csv", "output")

    assert result.returncode == 0   

    with open("./data/messages.csv", 'r') as f:
        lines = f.readlines()
        first_message = lines[1].split(',') #skip header to get first message
        expected_id = first_message[0]
    
    json_file = f"output/{expected_id}.json"
    data = load_json_file(json_file)
    
    assert data["id"] == expected_id


def test_F07_date_format_conversion():
    messages_csv = """id,datetime,direction,content,contact
bccfe3e5-f89d-4859-ad53-dea6f556cf28,1770050100,originating,Test message F07,1009"""
    
    contacts_csv = """id,name
1009,Test Contact"""
    
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)

    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode == 0   

    data = load_json_file("output/bccfe3e5-f89d-4859-ad53-dea6f556cf28.json")
    
    # 1770050100 corresponds to 2026-02-02T16:35:00 UTC (checked with an epoch converter)
    expected_datetime = "2026-02-02T16:35:00"
    assert data["datetime"] == expected_datetime


def test_F08_content_encoding():
    test_content = "Hello World"
    messages_csv = f"""id,datetime,direction,content,contact
6cf156bb-5baa-4113-ade1-f78b8be86862,1770050100,originating,{test_content},1010"""
    
    contacts_csv = """id,name
1010,Test Contact"""

    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)

    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode == 0   

    data = load_json_file("output/6cf156bb-5baa-4113-ade1-f78b8be86862.json")

    decoded_content = base64.b64decode(data["content"]).decode('utf-8')
    assert decoded_content == test_content



def test_F09_contact_resolution():
    messages_csv = """id,datetime,direction,content,contact
93e1b4ff-e0d7-4ee0-bf66-ee5739f41944,1770064857,originating,Test Message,1110"""

    contacts_csv = """id,name
1110,Contact found"""

    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)

    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")

    assert result.returncode == 0   

    data = load_json_file("output/93e1b4ff-e0d7-4ee0-bf66-ee5739f41944.json")

    assert data["contact"] == "Contact found"


def test_F10_extra_columns_handling():
    messages_csv = """id,datetime,direction,content,contact,extra_column
0d52a65b-5baa-4079-ad11-12f75956f2d8,1770066080,originating,Test extra,1011,ignored"""
    
    contacts_csv = """id,name,email,phone
1011,Test Contact,test@example.com,+33123456789"""

    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)

    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    
    assert result.returncode == 0   

    data = load_json_file("output/0d52a65b-5baa-4079-ad11-12f75956f2d8.json")

    expected_fields = {"id", "datetime", "direction", "content", "contact"}
    actual_fields = set(data.keys())

    assert actual_fields == expected_fields


def test_F11_max_output_limit():
    msg_lines = ["id,datetime,direction,content,contact"]
    nb_messages = 50
    for i in range(nb_messages):
        msg_lines.append(f"{str(uuid.uuid4())},1770138198,originating,Message {i},1001")
    
    contacts_csv = """id,name
1001,Test Contact"""
    
    create_test_csv("./data/test_messages.csv", "\n".join(msg_lines))
    create_test_csv("./data/test_contacts.csv", contacts_csv)

    run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    
    generated_files = os.listdir("output")
    
    assert len(generated_files) == nb_messages, f"Expected {nb_messages} files created, found {len(generated_files)}"