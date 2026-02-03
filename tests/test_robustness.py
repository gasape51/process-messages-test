import base64
import subprocess
import os
import shutil
import json 
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
    """Helper to run the process_messages program"""
    result = subprocess.run(
        ["./process_messages", messages_file, contacts_file, output_dir],
        capture_output=True,
        text=True
    )
    return result


# Robustness test cases
def test_R01_missing_messages_file():
    result = run_process_messages("./data/non_existent_messages.csv", "./data/contacts.csv", "output")
    assert result.returncode != 0 


def test_R02_missing_contacts_file():
    result = run_process_messages("./data/messages.csv", "./data/non_existent_contacts.csv", "output")
    assert result.returncode != 0  


def test_R03_missing_argument():
    result = subprocess.run(
        ["./process_messages", "./data/messages.csv", "./data/contacts.csv"],
        capture_output=True
    )
    assert result.returncode != 0

def test_R04_empty_messages_file():
    messages_csv = """id,datetime,direction,content,contact
"""
    create_test_csv("./data/test_messages.csv", messages_csv)

    result = run_process_messages("./data/test_messages.csv", "./data/contacts.csv", "output")

    assert result.returncode == 0  
    assert len(os.listdir("output")) == 0


def test_R05_missing_contact():
    messages_csv = """id,datetime,direction,content,contact
5006f8c8-52b2-4d5b-9820-90e25adf7d53,1770108032,originating,Test missing contact,9999"""
    
    contacts_csv = """id,name
1011,Test Contact"""

    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)

    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    
    assert result.returncode != 0

def test_R06_missing_content_column():
    messages_csv = """id,datetime,direction,contact
6b457f09-4f5c-46a3-9f76-369e0bdf14a2,1770110080,originating,1001"""

    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    
    assert result.returncode != 0

def test_R07_missing_datetime_column():
    messages_csv = """id,direction,content,contact
6059bcd8-63a7-4a00-bc9b-658c3430a370,originating,Test missing datetime,1001"""

    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)   
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    
    assert result.returncode != 0

def test_R08_missing_content_field():
    messages_csv = """id,datetime,direction,content,contact
e5579dcb-1422-45fc-9b0f-d565e045bdd8,1770123456,originating,,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0

def test_R09_missing_id_field():
    messages_csv = """id,datetime,direction,content,contact
,1770135791,originating,Test missing id,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0

def test_R10_missing_datetime_field():
    messages_csv = """id,datetime,direction,content,contact
f433528e-ab80-44d9-b84b-b0580e87fca7,,originating,Test missing datetime,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0

def test_R11_missing_contact_field():
    messages_csv = """id,datetime,direction,content,contact
81d5041b-2166-4fff-9541-d4719507e30d,1770112860,originating,Test missing contact,"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    
    assert result.returncode != 0
    
def test_R12_special_characters_in_content():
    special_content = "Message with special characters: émojis 😀 and symboles #@&`~"
    messages_csv = f"""id,datetime,direction,content,contact
a33c4379-76e8-4b4b-a15e-3302279588d6,1770114487,originating,{special_content},1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode == 0
    
def test_R13_timestamp_before_epoch():
    messages_csv = """id,datetime,direction,content,contact
eac1d209-9f68-4856-aed0-eedff504bd0d,-86400,originating,Test timestamp before epoch,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    
    assert result.returncode == 0 
    json_file = "output/eac1d209-9f68-4856-aed0-eedff504bd0d.json"
    assert os.path.exists(json_file)

def test_R14_invalid_direction_field():
    messages_csv = """id,datetime,direction,content,contact
3897058c-d665-4ecf-a231-e29da5715568,1770116018,invalid_direction,Test invalid direction,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0

def test_R15_invalid_csv_separator():
    messages_csv = """id;datetime;direction;content;contact
1baa2d8e-8d1d-4a9e-b478-8367aebf75b9;1770118526;originating;Test invalid CSV separator;1001"""
    contacts_csv = """id;name
1001;Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0

def test_R16_comma_in_content_field():
    messages_csv = """id,datetime,direction,content,contact
dbdc08af-4a6c-4766-b35c-f9b5dc1bbcd1,1770118885,originating,"Message with, comma in content",1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)   
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode == 0

def test_R17_messages_with_same_id():
    messages_csv = """id,datetime,direction,content,contact
1841efe3-6703-4450-8372-deeec6624350,1770119260,originating,First message with duplicate ID,1001
1841efe3-6703-4450-8372-deeec6624350,1770119265,originating,Second message with duplicate ID,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0  
    assert len(os.listdir("output")) == 2 # ?? to discuss at interview

def test_R18_missing_header_row_messages():
    messages_csv = """f8485a27-4488-40b4-adbd-7ebaf63d401c,1770119757,originating,Test missing header row,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0

def test_R19_invalid_ID_format():
    messages_csv = """id,datetime,direction,content,contact
12345,1770120200,originating,Test invalid ID format,1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0   

def test_R20_invalid_contact_field_type():
    messages_csv = """id,datetime,direction,content,contact
a0a8ef8e-534c-4202-aa79-5950d2cc6c60,1770120830,originating,Test invalid contact type,not_a_valid_contact_id"""
    contacts_csv = """id,name
not_a_valid_contact_id,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode != 0

def test_R21_large_content_field():
    large_content = "A" * 1000000  
    messages_csv = f"""id,datetime,direction,content,contact
d2f5c3e1-3c4b-4f5a-b6e1-2f3c4d5e6f7a,1770121450,originating,{large_content},1001"""
    contacts_csv = """id,name
1001,Test Contact"""
    create_test_csv("./data/test_messages.csv", messages_csv)
    create_test_csv("./data/test_contacts.csv", contacts_csv)
    result = run_process_messages("./data/test_messages.csv", "./data/test_contacts.csv", "output")
    assert result.returncode == 0
