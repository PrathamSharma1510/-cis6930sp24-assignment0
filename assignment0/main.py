import argparse
import urllib.request
import os
import sqlite3
import pandas as pd
import fitz  # PyMuPDF
import re

def download_pdf(url, save_path='/tmp/incident_report.pdf'):
    """Download PDF from a specified URL to a local file path."""
    headers = {'User-Agent': "Mozilla/5.0"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    
    with open(save_path, 'wb') as file:
        file.write(data)
        
        
    return save_path

def extract_incidents_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ""
    for page in doc:
        all_text += page.get_text()
    doc.close()

    lines = all_text.split('\n')
    data = {'Date/Time': [], 'Incident Number': [], 'Location': [], 'Nature': [], 'Incident ORI': []}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if '/' in line and ':' in line:  # Likely a 'Date/Time' entry
            data['Date/Time'].append(line)
            i += 1  # Move to the next line for 'Incident Number'
            
            # Ensure subsequent values are captured or set to 'NULL' if not present or if the next record starts
            for field in ['Incident Number', 'Location', 'Nature', 'Incident ORI']:
                # if field == 'Nature' and 'RAMP' in lines[i].upper():
                #         data[field].append(lines[i+1].strip() if lines[i+1].strip() else "null")
                if i < len(lines) and not ('/' in lines[i] and ':' in lines[i]):
                    if(field=='Nature' and lines[i]=="RAMP"):
                        data[field].append(lines[i+1].strip() if lines[i+1].strip() else "null")
                    else:
                        data[field].append(lines[i].strip() if lines[i].strip() else "null")
                    i += 1
                else:
                    # If the expected value is missing, append 'NULL' and do not increment 'i'
                    data[field].append("null")
        else:
            # If the line doesn't match the expected start of a new record, increment 'i' to check the next line
            i += 1

    # Validate lengths of lists before creating DataFrame
    if not all(len(lst) == len(data['Date/Time']) for lst in data.values()):
        raise ValueError("Error: Mismatch in list lengths within the data dictionary.")
    
    if data['Date/Time']:  # Ensure there's at least one record
        for key in data:
            data[key].pop(-1)
    return pd.DataFrame(data)


def create_db_and_table(db_path):
    """Create SQLite database and incidents table if they do not exist."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        );
    ''')
    conn.commit()
    conn.close()

def populate_db(db_path, df):
    """Insert DataFrame records into the SQLite database."""
    conn = sqlite3.connect(db_path)
    df.to_sql('incidents', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def print_incident_summary(db_path):
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT COALESCE(nature, '') AS nature, COUNT(*) AS count
    FROM incidents
    GROUP BY nature
    ORDER BY count DESC, nature ASC;
    '''
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    
    for nature, count in rows:
        # Print the 'Nature' as is, which will be an empty string if it was 'NULL' or empty
        if(nature == 'null'):
             print(f"|{count}")
        else:
            print(f"{nature if nature else ' '} | {count}")


def main(url, db_path='resources/normanpd.db'):
    if not os.path.exists('resources'):
        os.makedirs('resources')
        
    pdf_path = download_pdf(url)
    incidents_df = extract_incidents_from_pdf(pdf_path)
    create_db_and_table(db_path)
    populate_db(db_path, incidents_df)
    print_incident_summary(db_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process incident data from a PDF.")
    parser.add_argument("--incidents", type=str, required=True, help="URL to the incident summary PDF.")
    args = parser.parse_args()
    main(args.incidents)

