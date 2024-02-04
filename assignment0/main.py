# main.py
import argparse
import urllib.request
import os
from PyPDF2 import PdfReader
import re
import sqlite3
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
    reader = PdfReader(pdf_path)
    text = reader.pages[0].extract_text()
    # print(text)
    incidents = []

    
    pattern = re.compile(r'(\d+/\d+/\d+ \d+:\d+) (\d{4}-\d{8}) (.*?) (Traffic Stop|Chest Pain|Sick Person|Motorist Assist|Burglary|Shots Heard|Alarm|Disturbance/Domestic|Fire Dumpster|Shooting Stabbing Penetrating) ([A-Z0-9]+)$', re.IGNORECASE)

    for page in reader.pages:
        text = page.extract_text()
        lines = text.split('\n')
        
        for line in lines:
            match = pattern.search(line)
            if match:
                incidents.append({
                    'date_time': match.group(1),
                    'incident_number': match.group(2),
                    'location': match.group(3).strip(),
                    'nature': match.group(4).strip(),
                    'incident_ori': match.group(5)
                })

    # for incident in incidents:
    #     print(incident)
    return incidents

def createdb(db_path):
    # Connect to the SQLite database. This will create the database file if it doesn't exist
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create the incidents table
    c.execute('''
    CREATE TABLE IF NOT EXISTS incidents (
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
    
def populate_db(db_path, incidents):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Insert each incident into the incidents table
    for incident in incidents:
        c.execute('''
        INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
        VALUES (?, ?, ?, ?, ?);
        ''', (incident['date_time'], incident['incident_number'], incident['location'], incident['nature'], incident['incident_ori']))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def main(url):
    # Download data
    db_path = 'resources/normanpd.db'  # Make sure this path is correct
    
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
    # assignment0.print_status(db)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process incident data.")
    parser.add_argument("--incidents", type=str, required=True, help="URL to the incident summary PDF.")
    
    args = parser.parse_args()
    main(args.incidents)
