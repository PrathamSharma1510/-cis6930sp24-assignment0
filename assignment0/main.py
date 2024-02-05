# main.py
import argparse
import urllib.request
import os
from PyPDF2 import PdfReader
import re
import fitz # PyMuPDF
import sqlite3
import pandas as pd
# from assignment0 import datafetch as data_fetch
def fetchincidents(url):
    # Specify the user agent to avoid blocking by some websites
    # url = ("https://www.normanok.gov/sites/default/files/documents/"
    #    "2024-01/2024-01-01_daily_incident_summary.pdf")
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

    # Create a request object with the given URL and headers
    request = urllib.request.Request(url, headers=headers)

    # Use urllib to open the URL and read the data
    response = urllib.request.urlopen(request)
    data = response.read()
    # print(data)
    # Define the path for saving the PDF, using /tmp for temporary storage
    file_path = '/tmp/incident_report.pdf'

    # Write the downloaded PDF to a file
    with open(file_path, 'wb') as file:
        file.write(data)
        
    return file_path
def extract_incidents(pdf_path):
    doc = fitz.open("/tmp/incident_report.pdf")

    all_text = ""
    for page in doc:
        all_text += page.get_text()

    doc.close()

    lines = all_text.split('\n')

    date_times, incident_numbers, locations, natures, incident_oris = [], [], [], [], []

    for i in range(0, len(lines)):
        if 'Date / Time' in lines[i]: 
            continue
        
        if i + 4 < len(lines) and '/' in lines[i] and ':' in lines[i]:
            date_times.append(lines[i].strip())
            incident_numbers.append(lines[i + 1].strip())
            locations.append(lines[i + 2].strip())
            natures.append(lines[i + 3].strip())
            incident_oris.append(lines[i + 4].strip())

    
    df = pd.DataFrame({
        'Date/Time': date_times,
        'Incident Number': incident_numbers,
        'Location': locations,
        'Nature': natures,
        'Incident ORI': incident_oris
    })

    return df
    # reader = PdfReader(pdf_path)
    # text = reader.pages[0].extract_text()
    # # print(text)
    # incidents = []
    # reader = PdfReader(pdf_path)
    # incidents = []

    # # Assuming 'incident_ori' has a recognizable pattern, like a set of alphanumeric characters.
    # # This pattern is designed to be more forgiving by capturing any text for the 'nature'
    # # until it encounters a known pattern for 'incident_ori'.
    # pattern = re.compile(r'(\d+/\d+/\d+ \d+:\d+) (\d{4}-\d{8}) (.*?) ([\w\s]+) ([A-Z0-9]{8})$', re.IGNORECASE)

    # for page in reader.pages:
    #     text = page.extract_text()
    #     lines = text.split('\n')
        
    #     for line in lines:
    #         match = pattern.search(line)
    #         if match:
    #             incidents.append({
    #                 'date_time': match.group(1),
    #                 'incident_number': match.group(2),
    #                 'location': match.group(3).strip(),
    #                 # The nature is now more flexibly captured
    #                 'nature': match.group(4).strip(),
    #                 'incident_ori': match.group(5)
    #             })

    # return incidents

def createdb(db_path):
  # Connect to the SQLite database or create a new one if it doesn't exist
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check if the "incidents" table exists in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    table_exists = c.fetchone()
    
    if not table_exists:
        # Create the incidents table if it doesn't exist
        c.execute('''
        CREATE TABLE incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        );
        ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
def populate_db(db_path, df):
    # Connect to the SQLite database using the correct db_path
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Clear the existing records in the table (optional, based on your requirement)
    cur.execute("DELETE FROM incidents")
    
    # Insert new records from the DataFrame
    for _, row in df.iterrows():
        cur.execute(
            '''
            INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (row['Date/Time'], row['Incident Number'], row['Location'], row['Nature'], row['Incident ORI'])
        )
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()

    # # Insert each incident into the incidents table
    # for incident in incidents:
    #     c.execute('''
    #     INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
    #     VALUES (?, ?, ?, ?, ?);
    #     ''', (incident['date_time'], incident['incident_number'], incident['location'], incident['nature'], incident['incident_ori']))

    # # Commit the changes and close the connection
    # conn.commit()
    # conn.close()

def print_status(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = '''
    SELECT nature, COUNT(nature) AS cnt
    FROM incidents
    GROUP BY nature
    ORDER BY cnt DESC, nature ASC;
    '''
    c.execute(query)
    results = c.fetchall()
    
    for nature, count in results:
        print(f'{nature}|{count}')
    
    conn.close()


def main(url):
    # import time
    # timestamp = time.strftime("%Y%m%d%H%M%S")
    db_path = f'resources/normanpd.db'
    # Download dataure this path is correct
    
    # Ensure the resources directory exists
    if not os.path.exists('resources'):
        os.makedirs('resources')
    incident_data = fetchincidents(url)
    # Extract data
    incidents = extract_incidents(incident_data)
    
    # # Create new database
    db = createdb(db_path)
    
    # # Insert data
    populate_db(db_path, incidents)
    
    # # Print incident counts
    print_status(db_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process incident data.")
    parser.add_argument("--incidents", type=str, required=True, help="URL to the incident summary PDF.")
    
    args = parser.parse_args()
    main(args.incidents)
