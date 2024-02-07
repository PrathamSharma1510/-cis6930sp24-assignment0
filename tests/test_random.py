
import pandas as pd
import sqlite3
import os
from assignment0.main import extract_incidents_from_pdf, create_db_and_table, populate_db  # Replace 'your_module' with the actual module name

# Test extract_incidents_from_pdf
def test_extract_incidents_from_pdf():
    pdf_path = 'docs/test.pdf'  # Replace with the path to your test PDF
    df = extract_incidents_from_pdf(pdf_path)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # Add more assertions based on known test PDF structure and content

# Test create_db_and_table
def test_create_db_and_table(tmpdir):
    db_path = os.path.join(tmpdir, 'test_db.sqlite')
    create_db_and_table(db_path)
    assert os.path.exists(db_path)
    # Check if table exists
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('incidents',) in tables
    conn.close()

# Test populate_db
def test_populate_db(tmpdir):
    db_path = os.path.join(tmpdir, 'test_db.sqlite')
    create_db_and_table(db_path)  # Make sure the table is created first
    test_data = {
        'Date/Time': ['01/01/2023 00:00'],
        'Incident Number': ['0000001'],
        'Location': ['Some Location'],
        'Nature': ['Some Nature'],
        'Incident ORI': ['Some ORI']
    }
    test_df = pd.DataFrame(test_data)
    populate_db(db_path, test_df)
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM incidents", conn)
    conn.close()
    assert not df.empty
    # Add more detailed checks to verify data integrity

# You can run the test with pytest
# pytest -v test_your_test_file.py
